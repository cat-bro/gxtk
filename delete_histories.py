import argparse
from utils import get_galaxy_instance

"""
Delete histories belonging to user
"""

def main():
    parser = argparse.ArgumentParser(description='Delete user histories')
    parser.add_argument('--name_startswith', help='History name prefix')
    parser.add_argument('--days_since_updated', type=int, help='Last updated more than X days ago')
    parser.add_argument('--delete_all', type=int, help='In the absence of conditions include this argument to delete all histories')
    parser.add_argument('-g', '--galaxy_url', help='URL of Galaxy instance')
    parser.add_argument('-a', '--api_key', help='Galaxy api key')
    parser.add_argument('-p', '--profile', help='Key for profile set in profiles.yml')
    args = parser.parse_args()

    if not args.name_startswith or args.days_since_updated or args.delete_all:
        print("Command needs one of --name_startswith, --days_since_updated or --delete_all")
        return
    
    if args.delete_all and (args.name_startswith or args.days_since_updated):
        print("--delete_all cannot be combined with filtering conditions")
        return

    if args.days_since_updated:
        print("--days_since_updated logic has not been implemented")
        return

    galaxy_instance = get_galaxy_instance(args.galaxy_url, args.api_key, args.profile)

    histories = galaxy_instance.histories.get_histories()[::-1]

    histories = list(filter(lambda x: not x['deleted'], histories))
    if args.name_startswith:
        histories = list(filter(lambda x: x['name'].startswith(args.name_startswith), histories))

    num_histories_to_delete = len(histories)
    print(f'{num_histories_to_delete} to delete')
    for x, history in enumerate(histories):
        galaxy_instance.histories.delete_history(history['id'], purge=True)
        if x%20 == 0 or x == num_histories_to_delete - 1:
            print(f'Deleted {x}/{num_histories_to_delete} histories')


if __name__ == "__main__":
    main()
