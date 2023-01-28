import subprocess
from dataclasses import dataclass

COMMAND = 'winget upgrade'
EXCLUDED_LIST = (
    'JetBrains.DataGrip',
    'JetBrains.PyCharm.Professional',
    'JetBrains.DataGrip',
    'JetBrains.GoLand',
)


@dataclass
class Program:
    name: str
    program_id: str
    version: str
    available: str
    source: str


def get_program() -> list[Program]:
    output = subprocess.run(
        COMMAND, capture_output=True
    ).stdout.decode('utf-8')
    lines = output[output.index('Name'):].split('\r\n')
    header = lines[:2]
    delimiter = f'---{header[1]}'
    print()
    print('# ', header[0])
    print(delimiter)
    id_index = lines[0].index('Id')
    programs_list = []
    for line in lines[2:-2]:
        name = line[:id_index].strip()
        program_id, t_line = line[id_index:].split(' ', 1)
        if program_id in EXCLUDED_LIST:
            continue
        t_line, source = t_line.strip().rsplit(' ',  1)
        version, available = t_line.strip().rsplit(' ', 1)
        programs_list.append(
            Program(name, program_id, version, available, source)
        )
        print(f'{len(programs_list):<3}{line}')
    print(delimiter)
    print(f'\n{len(programs_list)} upgrades available.\n')
    return programs_list


def update_program(program_id: str):
    subprocess.run(f'{COMMAND} {program_id}')


if __name__ == '__main__':
    programs_list = get_program()
    if input('Update all programs?[Y/n]: ').lower() in ('y', 'yes', ''):
        for program in programs_list:
            update_program(program.program_id)
