import requests
import attr
# import time


@attr.s
class PackageInfo(object):
    name = attr.ib(type=str)
    search_version = attr.ib(type=str, default=None)
    search_version_release_date = attr.ib(type=str, default=None)
    pypi_json = attr.ib(type=dict, init=False)
    release_version = attr.ib(type=str, init=False)
    release_date = attr.ib(type=str, init=False)

    def _get_release_version(self):
        return self.pypi_json['info']['version']

    def _get_release_date(self) -> str:
        return self.pypi_json['releases'][self.release_version][0]['upload_time']

    def _get_version_release_date(self) -> str:
        return self.pypi_json['releases'][self.release_version][0]['upload_time']

    def _call_pypi(self) -> requests.Response:
        base_url = f"https://pypi.org/pypi/{self.name}/json"
        response = requests.get(base_url)
        return response

    def __attrs_post_init__(self):
        self.pypi_json = self._call_pypi().json()
        self.release_version = self._get_release_version()
        self.release_date = self._get_release_date()

        if self.search_version:
            self.search_version_release_date = self._get_version_release_date()

    def time_passed_since_update(self) -> str:
        # TODO should this be Maya formatted?
        # if version given, it should be from there.
        # time.time()
        pass

