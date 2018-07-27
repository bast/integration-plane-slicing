"""
Integration plane is spanned by 3 points (p1, p2, p3) or two vectors (u and v):
    u = p2 - p1
    v = p3 - p1
Example usage:
    $ python slice.py template.inp u 5
This creates 5 files where the integration plane
is sliced up along the u vector:
    template_0.inp
    template_1.inp
    template_2.inp
    template_3.inp
    template_4.inp
"""

import sys
import os
from copy import deepcopy


def integration_parameters(input_lines):
    """
    .2D_INT
    p1_x p1_y p1_z
    p2_x p2_y p2_z
    k
    p3_x p3_y p3_z
    l
    m
    """
    i = input_lines.index('.2D_INT')

    p1 = tuple(map(lambda x: float(x), input_lines[i+1].split()))
    p2 = tuple(map(lambda x: float(x), input_lines[i+2].split()))
    p3 = tuple(map(lambda x: float(x), input_lines[i+4].split()))

    u = [p2[0] - p1[0],
         p2[1] - p1[1],
         p2[2] - p1[2]]
    v = [p3[0] - p1[0],
         p3[1] - p1[1],
         p3[2] - p1[2]]

    k = int(input_lines[i+3])
    l = int(input_lines[i+5])
    m = int(input_lines[i+6])

    return p1, u, v, k, l, m


def read_file(file_name):
    with open(file_name, 'r') as f:
        input_lines = f.read().splitlines()
    return input_lines


if __name__ == '__main__':
    file_name = sys.argv[-3]
    if not os.path.exists(file_name):
        sys.stderr.write('ERROR file {0} not found\n'.format(file_name))
        sys.exit(1)

    basename, extension = os.path.splitext(file_name)

    vector = sys.argv[-2]
    allowed_vectors = ['u', 'v']
    assert vector in allowed_vectors
    coordinate = allowed_vectors.index(vector)

    num_slices = int(sys.argv[-1])

    input_lines = read_file(file_name)

    i = input_lines.index('.2D_INT')
    up_to_2d_keyword = input_lines[:i+1]
    after_2d_keyword = input_lines[i+7:]

    p1, u, v, k, l, m = integration_parameters(input_lines)

    uv = [u, v]
    uv_ = deepcopy(uv)
    f = 1.0/num_slices
    uv_[coordinate] = [f*uv_[coordinate][0],
                       f*uv_[coordinate][1],
                       f*uv_[coordinate][2]]
    u_ = uv_[0]
    v_ = uv_[1]

    for s in range(num_slices):
        f = s/num_slices
        p1_ = (p1[0] + f*uv[coordinate][0],
               p1[1] + f*uv[coordinate][1],
               p1[2] + f*uv[coordinate][2])
        p2_ = (p1_[0] + u_[0],
               p1_[1] + u_[1],
               p1_[2] + u_[2])
        p3_ = (p1_[0] + v_[0],
               p1_[1] + v_[1],
               p1_[2] + v_[2])

        with open('{0}_{1}{2}'.format(basename, s, extension), 'w') as f:
            f.write('\n'.join(up_to_2d_keyword))
            f.write('\n')
            f.write('{0} {1} {2}\n'.format(p1_[0], p1_[1], p1_[2]))
            f.write('{0} {1} {2}\n'.format(p2_[0], p2_[1], p2_[2]))
            f.write('{0}\n'.format(k))
            f.write('{0} {1} {2}\n'.format(p3_[0], p3_[1], p3_[2]))
            f.write('{0}\n'.format(l))
            f.write('{0}\n'.format(m))
            f.write('\n'.join(after_2d_keyword))
            f.write('\n')
