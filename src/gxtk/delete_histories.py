import time
import datetime as dt
from bioblend import ConnectionError

timeout = 60*60*6 # will time out eventually after waiting 6 hours for a single history
datetime_format = '%Y-%m-%dT%H:%M:%S.%f'
wait_patiently = True # TODO make this a parameter

"""
Delete histories belonging to user.  This will wait for small histories that can be deleted within 2-3 minutes.
For histories that take longer than nginx takes to time out, the script waits until the history has state 'deleted'
unless the --skip_wait flag is included in the command.
"""

def more_than_x_days_old(history, days):
    update_time = dt.datetime.strptime(history['update_time'], datetime_format)
    if dt.datetime.utcnow() - update_time > dt.timedelta(days=days):
        return True
    return False

def delete_histories(galaxy_instance, args):
    wait_patiently = not args.skip_wait
    if not (args.name_startswith or args.days_since_updated or args.delete_all):
        print("Command needs one of --name_startswith, --days_since_updated or --delete_all")
        return
    
    if args.delete_all and (args.name_startswith or args.days_since_updated):
        print("--delete_all cannot be combined with filtering conditions")
        return

    user = galaxy_instance.config.whoami()
    user_email = user['email']
    user_id = user['id']

    if args.user_email and not user_email == args.user_email:
        raise Exception('User email {args.user_email} was provided and does not match authenticated user email {user_email}')

    # TODO: wait for galaxy here
    histories = galaxy_instance.histories.get_histories(deleted=False, published=False)[::-1]

    if args.name_startswith:
        histories = list(filter(lambda x: x['name'].startswith(args.name_startswith), histories))
    
    if args.days_since_updated:
        histories = list(filter(lambda x: more_than_x_days_old(x, args.days_since_updated), histories))

    num_histories_to_delete = len(histories)
    print(f'{num_histories_to_delete} histories to delete for user {user_email}')
    if not args.yes:
        answer = input("Type y/yes to and enter to continue")
        if not answer in ['y', 'yes']:
            raise Exception('Stopping in the absence of user confirmation')

    for x, history in enumerate(histories):
        # TODO: wait for galaxy here
        try:
            history = galaxy_instance.histories.show_history(history['id'])
            print(f'Deleting history {history["id"]} {history["name"]} last updated on {history["update_time"]}')
        except ConnectionError:
            print(f'\tError connecting to galaxy. Skipping history {history["name"]}')
            continue
        if not history['user_id'] == user_id:  # this isn't supposed to happen but just in case
            print(f'history user_id and user_id do not match, not deleting history {history["id"]}')
            continue
        try:
            galaxy_instance.histories.delete_history(history['id'], purge=True)
        except ConnectionError:
            if not wait_patiently:
                print(f'History {history["id"]} {history["name"]} will continue deleting in the background')
            else: # wait patiently
                print(f'Waiting for {history["id"]} {history["name"]} to be fully deleted')
                deleted = False
                start = dt.datetime.now()
                counter = 0
                while (dt.datetime.now() - start) < dt.timedelta(seconds=timeout) and not deleted:
                    try:
                        history = galaxy_instance.histories.show_history(history['id'])
                        deleted = history['deleted']
                    except ConnectionError:
                        print('\tError connecting to galaxy. Continuing to wait')
                    if not deleted:
                        time.sleep(60)
                        counter += 1  # any way of getting a measure of progress would be hard on the api
                        if counter > 0 and counter % 2 == 0:
                            print(f'\tStill waiting for history {history["id"]} {history["name"]} to be fully deleted') # TODO: print time

        if x > 0 and x%20 == 0 or x == num_histories_to_delete - 1:
            print(f'{x}/{num_histories_to_delete}')
