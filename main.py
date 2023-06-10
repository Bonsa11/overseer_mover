from multiprocessing.dummy import Pool
import os
import shutil
import argparse

argParser = argparse.ArgumentParser()
argParser.add_argument("-s", "--src", help="root path to copy from", required=True)
argParser.add_argument("-d", "--dst", help="root path to copy to", required=True)
argParser.add_argument("-t", "--threads", help="number of parallel threads", default=4, type=int)


def copy_or_down(src, dst):
    if not os.path.exists(dst):
        if os.path.isdir(src):
            try:
                shutil.copytree(src, dst)
            except Exception as e:
                print(f'failed to copy tree: {e}')
        else:
            try:
                if os.path.isfile(src):
                    shutil.copy(src, dst)
            except Exception as e:
                print(f'failed to copy file: {e}')
    else:
        if os.path.isdir(src):
            for child in os.listdir(src):
                copy_or_down(os.path.join(src, child), os.path.join(dst, child))


def try_multiple_threads(src, dst, fldrs):
    for fldr in fldrs:
        copy_or_down(os.path.join(src, fldr), os.path.join(dst, fldr))


def main():
    args = argParser.parse_args()

    if not os.path.exists(args.src):
        raise FileNotFoundError(f'cannot find src path {args.src}')

    if not os.path.exists(args.dst):
        raise FileNotFoundError(f'cannot find dst path {args.dst}')

    fldrs = os.listdir(args.src)

    if args.threads == 1:
        try_multiple_threads(args, fldrs)
    else:
        with Pool(args.threads) as p:
            p.starmap(try_multiple_threads, [(args.src, args.dst, fldr) for fldr in fldrs])


if __name__ == '__main__':
    main()
