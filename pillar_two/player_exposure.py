from sleeperpy import Drafts, User


def main():
    denis = User.get_user("akshathburra15")
    denis_drafts = Drafts.get_all_drafts_for_user('1126949978691207168',"nfl",2025)
    for draft in denis_drafts:
        print(draft)

main()