from attend_bananamall import attend as attend_bananamall
from attend_dingdong import attend as attend_dingdong
from attend_domaedoll import attend as attend_domaedoll
from attend_oname import attend as attend_oname
from attend_showdang import attend as attend_showdang
from attend_sofrano import attend as attend_sofrano
from attend_shoemarker import attend as attend_shoemarker
from attend_herotime import attend as attend_herotime
from utils import send_slack_message
from constants import TRY_COUNT

TEXT_TO_SLACK = ""

def run_attendance(site_name, func, headless=True):
    global TEXT_TO_SLACK

    for i in range(TRY_COUNT):
        try:
            print(f"\n▶️  [{i + 1}] {site_name} attendance started")
            func(headless)
            if i == TRY_COUNT - 2:
                TEXT_TO_SLACK += f"✅  {site_name} succeeded\n"
            elif i == TRY_COUNT - 1:
                TEXT_TO_SLACK += f"⚠️  {site_name} succeeded with retry, manual check recommended\n"
            break
        except Exception as e:
            print(f"\n❌  {site_name} error occured: {e}")
            if i == TRY_COUNT - 2:
                print(f"Retrying {site_name} attendance...")
            elif i == TRY_COUNT - 1:
                TEXT_TO_SLACK += f"❌  {site_name} failed after retries, manual check required\n"
                TEXT_TO_SLACK += f"\nError Log: {e}\n\n"
                

def main():
        # run_attendance("bananamall", attend_bananamall)
        # run_attendance("dingdong", attend_dingdong)
        # run_attendance("domaedoll", attend_domaedoll)
        # run_attendance("oname", attend_oname)
        # run_attendance("showdang", attend_showdang)
        run_attendance("sofrano", attend_sofrano)
        # run_attendance("shoemarker", attend_shoemarker)
        # run_attendance("herotime", attend_herotime)

        # send_slack_message(TEXT_TO_SLACK)
        # print("\n✅ message successfully sent to Slack, Exiting...")

if __name__ == "__main__":
    main()
