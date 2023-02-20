from math import ceil


def progressbar(current, max_val, width=30, include_progress_number=True,
                margins_fragment="|", pending_fragment=".", done_fragment="=", marker=">",
                ending_special="\r", leading_zero_progress=False, flush=False):
    """
    Draws a progressbar given current and max value.

    :param current:
    :param max_val:
    :param width:
    :param include_progress_number:
    :param margins_fragment:
    :param pending_fragment:
    :param done_fragment:
    :param marker:
    :param ending_special:
    :param leading_zero_progress:
    :param flush:
    :return:
    """

    percentage_completed = current / max_val

    done_segment = done_fragment * int(width * percentage_completed)
    pending_segment = pending_fragment * max(0,
                                             width - len(done_segment) -
                                             (1 - int(percentage_completed)) * ceil(percentage_completed))
    if include_progress_number:
        progress_number_segment = f" {current:{0 if leading_zero_progress else ''}{len(str(max_val))}}/{max_val}"
    else:
        progress_number_segment = ""
    constructed_string = \
        margins_fragment + \
        done_segment + \
        marker * (1 - int(percentage_completed)) * ceil(percentage_completed) + \
        pending_segment + \
        margins_fragment + \
        progress_number_segment

    # Sometimes it requires flush to be set to true. Apparently it has to do with the code buffering, but I'm not sure.
    print(constructed_string, end=ending_special, flush=flush)
    if current == max_val:
        print("\n")


