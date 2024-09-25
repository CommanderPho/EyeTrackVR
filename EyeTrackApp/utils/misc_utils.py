import os
import typing
import sys
import shutil
from pathlib import Path
from typing import Union

is_nt: bool = True if os.name == "nt" else False


def PlaySound(*args, **kwargs):
    pass


SND_FILENAME = SND_ASYNC = 1

if is_nt:
    import winsound

    PlaySound = winsound.PlaySound
    SND_FILENAME = winsound.SND_FILENAME
    SND_ASYNC = winsound.SND_ASYNC


def clamp(x, low, high):
    return max(low, min(x, high))


def lst_median(lst, ordered=False):
    # https://github.com/emilianavt/OpenSeeFace/blob/6f24efc4f58eb7cca47ec2146d934eabcc207e46/remedian.py
    assert lst, "median needs a non-empty list"
    n = len(lst)
    p = q = n // 2
    if n < 3:
        p, q = 0, n - 1
    else:
        lst = lst if ordered else sorted(lst)
        if not n % 2:  # for even-length lists, use mean of mid 2 nums
            q = p - 1
    return lst[p] if p == q else (lst[p] + lst[q]) / 2


class FastMedian:
    # https://github.com/emilianavt/OpenSeeFace/blob/6f24efc4f58eb7cca47ec2146d934eabcc207e46/remedian.py
    # Initialization
    def __init__(self, inits: typing.Optional[typing.Sequence] = [], k=64):  # after some experimentation, 64 works ok
        self.all, self.k = [], k
        self.more, self.__median = None, None
        if inits is not None:
            [self + x for x in inits]

    # When full, push the median of current values to next list, then reset.
    def __add__(self, x):
        self.__median = None
        self.all.append(x)  # It would be faster to pre-allocate an array and assign it by index.
        if len(self.all) == self.k:
            self.more = self.more or FastMedian(k=self.k)
            self.more + self.__medianPrim(self.all)
            # It's going to be slower because of the re-allocation.
            self.all = []  # reset

    #  If there is a next list, ask its median. Else, work it out locally.
    def median(self):
        return self.more.median() if self.more else self.__medianPrim(self.all)

    # Only recompute median if we do not know it already.
    def __medianPrim(self, all):
        if self.__median is None:
            self.__median = lst_median(all, ordered=False)
        return self.__median

def resource_path(relative_path: Union[str, Path]) -> str:
    """
    Get absolute path to resource, works for dev and for PyInstaller
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = Path(sys._MEIPASS)
    except AttributeError:
        base_path = Path(".")
    
    return str(base_path / relative_path)


class UserDataFolders:
    """ Provides consistent path to the user's data directory
    
    from utils.misc_utils import UserDataFolders
    
    """
    @classmethod
    def create_user_data_folder_if_needed(cls):
        # Determine the user's default directory
        if sys.platform == "win32":
            user_dir = os.environ.get('USERPROFILE', '')
        else:
            user_dir = os.environ.get('HOME', '')

        user_data_path = os.path.join(user_dir, 'EyeTrackVR', 'user_data')

        # Check if the user_data folder already exists
        if not os.path.exists(user_data_path):
            print(f'user_data_path: "{user_data_path}" does not exist. Creating from packaged configs...')
            # Get the path to the packaged user_data folder
            if getattr(sys, 'frozen', False):
                # If the application is frozen (packaged)
                app_dir = sys._MEIPASS
            else:
                # If the application is run directly
                app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # EyeTrackApp

            packaged_user_data = os.path.join(app_dir, '../user_data')

            # Copy the user_data folder to the user's default directory
            shutil.copytree(packaged_user_data, user_data_path)
            return True
        else:
            ## already exists
            return False

    @classmethod
    def resource_user_data_folder(cls, *other):
        """ Get absolute path to the user configs folder, or if *other is provided it will build the proper url for any files that are its contents.
        
        Usage:
        from utils.misc_utils import UserDataFolders
        
        user_data_folder: Path = UserDataFolders.resource_user_data_folder()
        
        """
        user_data_folder = Path(resource_path("user_data")).resolve()
        if ((not user_data_folder.exists()) or (not user_data_folder.is_dir())):
            user_data_folder = Path(resource_path("../user_data")).resolve() # look up a directory
        assert user_data_folder is not None
        assert user_data_folder.exists(), f"user_data: {user_data_folder}"
        # print(f'user_configs_folder: {user_configs_folder}')
        if len(other) == 0:
            return user_data_folder
        else:
            return user_data_folder.joinpath(*other).resolve()
        # return str(base_path / relative_path)



    @classmethod
    def resource_user_configs_folder(cls, *other):
        """ Get absolute path to the user configs folder, or if *other is provided it will build the proper url for any files that are its contents.
        
        Usage:
        from utils.misc_utils import UserDataFolders
        
        user_configs_folder: Path = UserDataFolders.resource_user_configs_folder()
        
        
        """
        user_data_folder = cls.resource_user_data_folder().resolve()
        assert user_data_folder.exists(), f"user_data_folder: {user_data_folder} does not exist"
        user_configs_folder = user_data_folder.joinpath('user_configs').resolve()
        assert user_configs_folder is not None
        assert user_configs_folder.exists(), f"user_configs_folder: {user_configs_folder} does not exist"
        # print(f'user_configs_folder: {user_configs_folder}')
        if len(other) == 0:
            return user_configs_folder
        else:
            return user_configs_folder.joinpath(*other).resolve()
        # return str(base_path / relative_path)
