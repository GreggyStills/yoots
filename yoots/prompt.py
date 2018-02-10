"""Functions for prompting users for input."""
from collections import OrderedDict
from getpass import getpass
import random
import time

from yoots import eprint


def confirm_yn(msg="Shall we do this thing? (y/n): "):
    """Ask user to enter yes/no, return True/False.  Repeat prompt if user reply is bogus.

    Args:
        msg (str):  Message prompting user for a yes or no answer

    Returns:
        confirmed: (bool)  True/False depending on user response
    """
    valid_replies = {'y': True, 'n': False}
    reply_valid = False
    confirmed = False
    while not reply_valid:
        reply = raw_input(msg).strip()[0].lower()
        if reply in valid_replies.keys():
            reply_valid = True
            confirmed = valid_replies[reply]
        else:
            eprint("\tERROR: Please respond with something that starts with y or n.")
    return confirmed


def confirm_countdown(msg="Will continue in [{}] seconds; press Ctrl-C to abort...", timeout=5):
    """Prompt user to press Ctrl-C or Enter before timeout.

    Args:
        msg (str): Message prompting user to press Ctrl-C before timeout, should contain '{}' for countdown
        timeout (int):  Seconds before countdown complete
    Returns:
        (bool) True=user didn't press Ctrl-C,  False=user pressed Ctrl-C
    """
    time_at_timeout = time.time() + timeout
    while time.time() < time_at_timeout:
        try:
            eprint(msg.format(timeout), newline='\r')
            timeout -= 1
            time.sleep(1)
        except KeyboardInterrupt:
            return False
    return True


def confirm_rnd(min_=100, max_=1000):
    """Have user confirm by entering a random integer.  If wrong, repeat prompt w/ new integer.

    Args:
        min_ (int): low number in random number range
        max_ (int): high number in random number range (actually max-1)
    Returns:
        confirmed (bool): Whether the user entered the right number
    """
    confirmed = False
    response = None
    msg = "Enter this number [ {} ] to confirm, or press Ctrl-C to cancel: "
    while not confirmed:
        rnd_int = random.choice(range(min_, max_))
        try:
            response = raw_input(msg.format(rnd_int)).strip()
            response = int(response)
        except (ValueError, TypeError):
            pass
        except KeyboardInterrupt:
            return False
        if response == rnd_int:
            confirmed = True
        else:
            eprint("\tERROR: Wrong number!")
    return confirmed


def ask_string(msg="Please enter a thingy I want: "):
    """Ask user to enter a string.  Returns whatever is entered, no further prompts.

    Args
        msg (str): Message prompting user for input
    Returns:
        response (str): Whatever the user entered
    """
    response = str(raw_input(msg))
    return response


def ask_string_confirm(msg="Please enter a thingy I want: "):
    """Ask user to enter a string, show them what we got, ask if it's correct.
    Even though they can see their entry as they type it, they could put extra spaces
    on the end, so we still want to show them what we got.

    Args:
        msg (str): Message prompting user for input
    Returns:
        result (str):  Whatever the user entered
    """
    confirmed = False
    response = None
    while not confirmed:
        response = ask_string(msg)
        confirmed = confirm_yn("You entered '{}'.\n\tIs this correct?: ".format(response))
    return response


def ask_string_secret(msg="Please enter a secret thingy I want (I will ask twice): "):
    """Ask user to enter a string, do not show it, and ask them to re-enter it.
    Repeat prompt if entries mismatch.

    Args:
        msg (str): Message prompting user for input
    Returns:
        result (str): Whatever the user entered
    """
    confirmed = False
    response = None
    while not confirmed:
        response = str(getpass(msg))
        response2 = str(getpass("Please re-enter: "))
        if response == response2:
            confirmed = True
        else:
            eprint("\tERROR: Your entries did not match.")
    return response


def pick_one(item_list=None, msg="Multiple options found, choose one."):
    """Prompt user to pick one item from an iterable (most commonly a list).

    Args:
        item_list (iterable): a list of items for user to choose from.
        msg: (str): Message to display before list selection.
    Returns:
        chosen: User-chosen item.
    """
    assert iter(item_list),\
        "ERROR: This function only accepts an iterable."
    chosen = None
    options = OrderedDict()
    for x, y in enumerate(item_list):
        options[str(x+1)] = y
    while not chosen:
        eprint("\n" + msg + "\n")
        for item_num, item in options.items():
            eprint("{}. {}".format(item_num, item))
        user_num = raw_input("\nEnter the item number you want: ").strip()
        chosen = options.get(user_num)
        if not chosen:
            eprint("\n\tERROR: That is not a valid selection!\n")
    return chosen


def pick_many(item_list=None, msg="Multiple options exist, choose all that apply."):
    """Prompt user to pick one or more items from a list.

    Args:
        item_list (iterable): a list of items for user to choose from.
        msg (str): Message to display before list selection.
    Returns:
        chosen (list): User-chosen items.
    """
    assert isinstance(item_list, list),\
        "ERROR: This function only accepts a list."
    chosen = []
    options = OrderedDict()
    for x, y in enumerate(item_list):
        options[str(x+1)] = y
    while not chosen:
        selection = []
        eprint("\n" + msg + "\n")
        for item_num, item in options.items():
            eprint("{}. {}".format(item_num, item))
        user_choice = raw_input(
            "\nEnter the item number(s) you want, separated by SPACE.  Or enter 'all' or 'none': ").lower()
        if 'all' in user_choice:
            return item_list
        elif 'none' in user_choice:
            return []
        else:
            selections = user_choice.split(' ')
            for selection in selections:
                item = options.get(selection)
                if item is None:
                    chosen = []
                    break
                else:
                    chosen.append(item)
        if not chosen:
            eprint("\n\tERROR: There is no [ {} ] on this list! You typed: '{}'".format(selection, user_choice))
    return chosen
