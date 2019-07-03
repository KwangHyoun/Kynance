

def print_line(content, length, fill_by='=', pre_len=False, post_len=False, center_opt=False):
    if pre_len+post_len+center_opt == 0:
        print('ERROR - At least one option must be entered.')
    if center_opt:
        return
    else:
        if pre_len == False:
            pre_len = length-len(content)-post_len-2
        if post_len == False:
            post_len = length-len(content)-pre_len-2
    pre = fill_by*pre_len+' '
    post = ' '+fill_by*post_len
    result = pre + content + post

    print(result)