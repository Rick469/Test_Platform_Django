def line_sum(lines, target, result=[]):
    if not lines:
        return result, False
    if not target:
        return result, True
    if target in lines:
        result.append(target)
        return result, True
    valid_lines = [l for l in lines if l <= target] # 排除大于target的元素
    if not valid_lines:
        return result, False
    suc = False     # 成功标记
    for line in valid_lines:
        line_target = target - line
        every_valid_lines = valid_lines[:]
        every_valid_lines.pop(valid_lines.index(line))
        if not line_target:
            result.append(line)
            suc = True
            return result, suc
        elif not every_valid_lines:
            suc = False
            return result, suc
        else:
            result.append(line)
            line_result, suc = line_sum(every_valid_lines, line_target, [])
            if not suc:
                result, suc = [], False
                continue
            else:
                result += line_result
                return result, suc
    return result, suc


