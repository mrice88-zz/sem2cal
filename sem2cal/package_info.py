import requests
import attr
import arrow

@attr.s
class PackageInfo(object):
    name = attr.ib(type=str)
    search_version = attr.ib(type=str, default=None)
    search_version_release_date = attr.ib(type=str, default=None)
    pypi_json = attr.ib(type=dict, init=False)
    release_version = attr.ib(type=str, init=False)
    release_date = attr.ib(type=str, init=False)
    release_name = attr.ib(type=str, init=False)
    package_author = attr.ib(type=str, init=False)
    package_author_email = attr.ib(type=str, init=False)
    package_maintainer = attr.ib(type=str, init=False)
    package_maintainer_email = attr.ib(type=str, init=False)
    license = attr.ib(type=str, init=False)

    def _get_release_version(self):
        return self.pypi_json['info']['version']

    def _get_release_date(self) -> str:
        return self.pypi_json['releases'][self.release_version][0]['upload_time']

    def _get_version_release_date(self) -> str:
        return self.pypi_json['releases'][self.release_version][0]['upload_time']

    def _get_author(self) -> str:
        return self.pypi_json['info']['author']

    def _get_author_email(self) -> str:
        return self.pypi_json['info']['author_email']

    def _get_maintainer(self) -> str:
        return self.pypi_json['info']['maintainer']

    def _get_maintainer_email(self) -> str:
        return self.pypi_json['info']['maintainer_email']

    def _get_license(self) -> str:
        return self.pypi_json['info']['license']

    def _get_release_name(self) -> str:
        return self.pypi_json['info']['name']

    def _call_pypi(self) -> requests.Response:
        base_url = f"https://pypi.org/pypi/{self.name}/json"
        response = requests.get(base_url)
        return response

    def __attrs_post_init__(self):
        self.pypi_json = self._call_pypi().json()
        self.release_version = self._get_release_version()
        self.release_date = self._get_release_date()
        self.license = self._get_license()
        self.release_name = self._get_release_name()

        if self.search_version:
            self.search_version_release_date = self._get_version_release_date()

        author = self._get_author()
        if author:
            self.package_author = author

        author_email = self._get_author_email()
        if author_email:
            self.package_author_email = author_email

        maintainer = self._get_maintainer()
        if maintainer:
            self.package_maintainer = maintainer

        maintainer_email = self._get_maintainer_email()
        if maintainer_email:
            self.package_maintainer_email = maintainer_email

    def time_passed_since_update(self, humanize: bool = False) -> str:
        if self.search_version_release_date:
            start_time = arrow.get(self.search_version_release_date)
        else:
            start_time = arrow.get(self.release_date)
        if humanize:
            time_passed = start_time.humanize(arrow.now())
        else:
            time_passed = str(arrow.utcnow() - start_time)

        return time_passed

