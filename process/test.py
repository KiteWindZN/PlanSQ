if __name__=='__main__':
    a=2.3
    b=1.2
    #c =((a-b) * 100) / 100
    #c =round((a-b), 5)
    d=1.1
    if(c == d):
        print("bbbb")
    print(c)
    print("aaaa")


def scan_lines(lines,vehicle):

    i=0
    N= len(lines)
    while i< N:
        if i < N-1:
            if lines[i].height==lines[i+1].height:
                lines[i].end.x= lines[i+1].end.x
                lines[i].width = round(lines[i].width,lines[i+1].width,5)

                lines.remove(lines[i+1])
                i=i-1
        i=i+1
        N=len(lines)

    for i in range(len(lines)):
        lines[i].height = lines[i].start.y
        lines[i].width = lines[i].end.x - lines[i].end.y

        if i==0:
            lines[i].left_height = vehicle.length - lines[i].height
        if i == len(lines)-1:
            lines[i].right_height = vehicle.lines - lines[i].height
        if i < len(lines) + 1:
            if lines[i].height < lines[i+1].height:
                lines[i].right_height = lines[i+1].height - lines[i].height
                lines[i+1].left_height = vehicle.length - lines[i+1].height
            else:
                lines[i].right_height = vehicle.length - lines[i].height
                lines[i + 1].left_height = lines[i].height - lines[i + 1].height
        if i > 0:
            if lines[i-1].height < lines[i].height:
                lines[i].left_height = vehicle.length - lines[i].height
                lines[i-1].right_height = lines[i].height - lines[i-1].height
            else:
                lines[i].left_height = lines[i-1].height - lines[i].height
                lines[i - 1].right_height = vehicle.length - lines[i - 1].height