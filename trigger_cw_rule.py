import boto3
import time
import logging
import argparse

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-unformatted_input', required=True, help="One string delimited by backticks")
    args = argparser.parse_args()
    cw_rule_name = args.unformatted_input

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    client = boto3.client('events')

    try:
        response = client.describe_rule(Name=cw_rule_name)
        schedule = response.get('ScheduleExpression', '')
        logging.info(f"Current schedule saved: {schedule}")
    except Exception as e:
        logging.error(f"Error retrieving schedule: {e}")
        exit(1)

    # Step 2: Update schedule to every 24 hours
    try:
        client.put_rule(
            Name=cw_rule_name,
            ScheduleExpression='rate(24 hours)',
            State='ENABLED'
        )
        logging.info("Schedule updated to every 24 hours")
    except Exception as e:
        logging.error(f"Error updating schedule: {e}")
        exit(1)

    # Step 3: Disable and enable the rule
    try:
        client.disable_rule(Name=cw_rule_name)
        logging.info("Rule disabled")
        time.sleep(1)
        client.enable_rule(Name=cw_rule_name)
        logging.info("Rule enabled")
    except Exception as e:
        logging.error(f"Error toggling rule state: {e}")
        exit(1)

    # Step 4: Sleep for 60 seconds
    time.sleep(60)

    # Step 5: Restore the original schedule
    try:
        client.put_rule(
            Name=cw_rule_name,
            ScheduleExpression=schedule,
            State='ENABLED'
        )
        logging.info("Original schedule restored")
    except Exception as e:
        logging.error(f"Error restoring original schedule: {e}")

    logging.info(f"Successfully invoked Schedule-based CloudWatch Rule: {cw_rule_name}")
