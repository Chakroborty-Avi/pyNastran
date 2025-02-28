from pyNastran.utils import PathLike

def parse_f06_geom(f06_filename: PathLike):
    """C A S E    C O N T R O L   D E C K   E C H O"""
    iline = 0
    nblank = 0
    is_section = False
    system_lines = []
    exec_lines = []
    case_lines = []
    bulk_lines = []
    with open(f06_filename, 'r') as f06_file:
        while nblank < 50:
            if not is_section:
                line = f06_file.readline().rstrip(); iline += 1
            if line == '':
                nblank += 1
                continue
            nblank = 0

            #print(f'A {iline}: {line!r}')
            if 'N A S T R A N    F I L E    A N D    S Y S T E M    P A R A M E T E R    E C H O' in line:
                iline, line = _get_geom_section(f06_file, iline, system_lines)
                is_section = True
            elif 'N A S T R A N    E X E C U T I V E    C O N T R O L    D E C K    E C H O' in line:
                iline, line = _get_geom_section(f06_file, iline, exec_lines)
                is_section = True
            elif 'C A S E    C O N T R O L   D E C K   E C H O' in line:
                iline, line = _get_geom_section(f06_file, iline, case_lines)
                is_section = True
            elif 'S O R T E D   B U L K   D A T A   E C H O' in line:
                iline, line = _get_geom_section(f06_file, iline, bulk_lines)
                is_section = True

            elif ('O U T P U T   F R O M   G R I D   P O I N T   W E I G H T   G E N E R A T O R' in line or
                  'R E A L   E I G E N V A L U E S' in line or
                  'R E A L   E I G E N V E C T O R   N O .' in line):
                break
            else:
                is_section = False
                #print('???')
                continue

                # while nblank < 50:
                #     line = f06_file.readline().rstrip(); iline += 1
                #     print('B', iline, line)
                #     if line == '':
                #         nblank += 1
                #         continue
                #     nblank = 0

    system_lines = [line.lstrip() for line in system_lines]
    exec_lines = [line.lstrip() for line in exec_lines]
    case_lines1 = [line.lstrip() for line in case_lines]
    case_lines = [line.split(' ', 1)[1].lstrip() for line in case_lines1 if ' ' in line]
    bulk_lines = [line.split('- ', 1)[1].lstrip() for line in bulk_lines if '-' in line] # 17-        CQUAD4

    # for i, linei in enumerate(system_lines):
    #     print(f'system {i}: {linei}')
    # for i, linei in enumerate(exec_lines):
    #     print(f'exec {i}: {linei}')
    # for i, linei in enumerate(case_lines):
    #     print(f'case {i}: {linei}')
    # for i, linei in enumerate(bulk_lines):
    #     print(f'bulk {i}: {linei}')
    #asdf
    return system_lines, exec_lines, case_lines, bulk_lines

def _get_geom_section(f06_file, iline: int, lines: list[str]) -> tuple[int, str]:
    line = ''
    nblank = 0
    #lines = []
    while not line.startswith('0'):
        line = f06_file.readline().rstrip(); iline += 1
        if len(line) > 1 and line.startswith('0'):
            #print(f'*** {line}')
            break
        if line == '':
            nblank += 1
            if nblank == 50:
                stopping
            continue
        nblank = 0
        if line == '0':
            line = ' 0'
            continue

        #print(f'aaa: {line.lstrip()!r}')
        strip_line = line.lstrip()
        if strip_line == 'CARD' or strip_line.startswith(('COUNT ', 'INPUT BULK DATA CARD COUNT')):
            continue
        lines.append(line)
    #print(lines)
    assert len(lines), lines
    return iline, line
