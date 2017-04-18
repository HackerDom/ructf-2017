from selenium.webdriver import PhantomJS
from selenium.common.exceptions import NoSuchElementException
from phantom_js import\
    get_driver, DriverInitializationException, DriverTimeoutException
import traceback
import sys


def init_get(command_ip, flag_id):
    try:
        with get_driver() as driver:
            return run_get_logic(driver, command_ip, flag_id)
    except DriverInitializationException as e:
        return {
            "code": 110,
            "private": "Couldn't init driver due to {} with {}".format(
                e, traceback.format_exc()
            )
        }
    except DriverTimeoutException as e:
        return {
            "code": 103,
            "public": "Service response timed out!",
            "private": "Service response timed out due to {}".format(e)
        }
    except Exception as e:
        return {
            "code": 110,
            "private": "ATTENTION!!! Unhandled error: {}".format(e)
        }


def run_get_logic(driver: PhantomJS, command_id, token):
    if not token:
        return {
            "code": 103,
            "public": "Session troubles!"
        }
    driver.add_cookie({
        'name': 'token',
        'value': token,
        'domain': "." + command_id.split(":")[0],
        'path': '/'
    })
    driver.get("http://{}/cabinet".format(command_id))
    try:
        flag_there = driver.find_element_by_xpath('//html//body//div//h5//i')
        flag_container = flag_there.get_attribute('innerHTML')
        return flag_container
    except NoSuchElementException as e:
        return "error_no_flag_in_cabinet"


if __name__ == '__main__':
    domain, token = sys.argv[1], sys.argv[2]
    get_result = init_get(domain, token)
    print(get_result)
