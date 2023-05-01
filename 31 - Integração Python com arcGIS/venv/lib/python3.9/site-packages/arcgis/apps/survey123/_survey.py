from __future__ import annotations
import os
import json
import time
import uuid
import tempfile
from urllib.parse import urlparse
from typing import Optional, Union, Any
import pandas as pd
from arcgis.gis import GIS, Item
from requests.utils import quote
import xml.etree.ElementTree as ET
from .exceptions import ServerError

########################################################################


class SurveyManager:
    """
    Survey Manager allows users and administrators of Survey 123 to
    analyze, report on, and access the data for various surveys.

    """

    _baseurl = None
    _gis = None
    _portal = None
    _url = None
    _properties = None
    # ----------------------------------------------------------------------

    def __init__(self, gis, baseurl=None):
        """Constructor"""
        if baseurl is None:
            baseurl = "survey123.arcgis.com"
        self._baseurl = baseurl
        self._gis = gis

    # ----------------------------------------------------------------------
    def __str__(self):
        return "< SurveyManager @ {iid} >".format(iid=self._gis._url)

    # ----------------------------------------------------------------------
    def __repr__(self):
        return self.__str__()

    # ----------------------------------------------------------------------
    @property
    def surveys(self) -> list:
        """returns a list of existing Survey"""
        query = (
            'type:"Form" AND NOT tags:"noxlsform"'
            'AND NOT tags:"draft" AND NOT typekeyw'
            "ords:draft AND owner:{owner}"
        ).format(owner=self._gis.users.me.username)
        content = self._gis.content
        items = content.search(
            query=query,
            item_type=None,
            sort_field="avgRating",
            sort_order="desc",
            max_items=10000,
            outside_org=False,
            categories=None,
            category_filters=None,
        )
        return [Survey(item=i, sm=self) for i in items]

    # ----------------------------------------------------------------------
    def get(self, survey_id: Union[Item, str]):
        """returns a single :class:`~arcgis.apps.survey123.Survey` object from and Item ID or Item"""
        if isinstance(survey_id, Item):
            survey_id = survey_id.id
        item = self._gis.content.get(survey_id)
        return Survey(item=item, sm=self)

    # ----------------------------------------------------------------------
    def _xform2webform(self, xform: str):
        """
        converts the xform xml to JSON for the item

        ============   ================================================
        *Inputs*       *Description*
        ------------   ------------------------------------------------
        xform          Required String. xform xml string
        ============   ================================================

        :returns: dict

        """
        url = "https://{base}/api/xform2webform".format(base=self._baseurl)
        params = {"xform": xform}
        return self._gis._con.post(
            path=url, postdata=params, files=None, verify_cert=False
        )

    # ----------------------------------------------------------------------
    def _xls2xform(self, file_path: str):
        """
        Converts a XLSForm spreadsheet to XForm XML. The spreadsheet must be in Excel XLS(X) format

        ============   ================================================
        *Inputs*       *Description*
        ------------   ------------------------------------------------
        file_path      Required String. Path to the XLS(X) file.
        ============   ================================================

        :returns: dict

        """

        url = "https://{base}/api/xls2xform".format(base=self._baseurl)
        params = {"f": "json"}
        file = {"xlsform": file_path}
        isinstance(self._gis, GIS)
        return self._gis._con.post(
            path=url, postdata=params, files=file, verify_cert=False
        )

    # ----------------------------------------------------------------------
    def _create(
        self,
        project_name: str,
        survey_item: Item,
        summary: str = None,
        tags: str = None,
    ) -> bool:
        """TODO: implement create survery from xls"""
        # XLS Item or File Path
        # https://survey123.arcgis.com/api/xls2xform
        ##Content-Disposition: form-data; name="xlsform"; filename="Form_2.xlsx"
        ##Content-Type: application/octet-stream
        # Create Folder
        # Create Feature Service
        # Update Feature layer and tables
        # Enable editor tracking
        # Update capabilities
        # Create web form
        # Create form item
        # Refresh ?
        return


########################################################################
class Survey:
    """
    A `Survey` is a single instance of a survey project. This class contains
    the :class:`~arcgis.gis.Item` information and properties to access the underlying dataset
    that was generated by the `Survey` form.

    Data can be exported to `Pandas DataFrames`, `shapefiles`, `CSV`, and
    `File Geodatabases`.

    In addition to exporting data to various formats, a `Survey's` data can
    be exported as reports.

    """

    _gis = None
    _sm = None
    _si = None
    _ssi = None
    _baseurl = None
    # ----------------------------------------------------------------------

    def __init__(self, item, sm, baseurl: Optional[str] = None):
        """Constructor"""
        if baseurl is None:
            baseurl = "survey123.arcgis.com"
        self._si = item
        self._gis = item._gis
        self._sm = sm
        try:
            self.layer_name = self._find_layer_name()
        except:
            self.layer_name = None
        self._baseurl = baseurl

        sd = self._si.related_items("Survey2Data", direction="forward")
        if len(sd) > 0:
            for item in sd:
                if "StakeholderView" in item.typeKeywords:
                    self._stk = item
                    _stk_layers = self._stk.layers + self._stk.tables
                    _idx = 0
                    if self.layer_name:
                        for layer in _stk_layers:
                            if layer.properties["name"] == self.layer_name:
                                _idx = layer.properties["id"]
                    self._stk_url = self._stk.url + f"/{str(_idx)}"

        related = self._si.related_items("Survey2Service", direction="forward")
        if len(related) > 0:
            self._ssi = related[0]
            self._ssi_layers = self._ssi.layers + self._ssi.tables
            _idx = 0
            if self.layer_name:
                for layer in self._ssi_layers:
                    if layer.properties["name"] == self.layer_name:
                        _idx = layer.properties["id"]
            self._ssi_url = self._ssi_layers[_idx]._url
            try:
                if self._ssi_layers[0].properties["isView"] == True:
                    view_url = self._ssi_layers[_idx]._url[:-1]
                    self.parent_fl_url = self._find_parent(view_url) + f"/{str(_idx)}"
            except KeyError:
                self.parent_fl_url = self._ssi_layers[_idx]._url

    # ----------------------------------------------------------------------
    @property
    def properties(self):
        """returns the properties of the survey"""
        return dict(self._si)

    # ----------------------------------------------------------------------
    def __str__(self):
        return "<Survey @ {iid}>".format(iid=self._si.title)

    # ----------------------------------------------------------------------
    def __repr__(self):
        return self.__str__()

    # ----------------------------------------------------------------------
    def download(
        self, export_format: str, save_folder: Optional[str] = None
    ) -> Union[str, pd.Dataframe]:
        """
        Exports the Survey's data to other format

        ================  ===============================================================
        **Parameter**      **Description**
        ----------------  ---------------------------------------------------------------
        export_format     Required String. This is the acceptable export format that a
                          user can export the survey data to. The following formats are
                          acceptable: File Geodatabase, Shapefile, CSV, and DF.
        ----------------  ---------------------------------------------------------------
        save_folder       Optional String. Specify the folder location where the output file should be stored.
        ================  ===============================================================

        :Returns: String or DataFrame
        """

        title = "a%s" % uuid.uuid4().hex
        if export_format.lower() == "df":
            return self._ssi.layers[0].query().sdf
        if save_folder is None:
            save_folder = tempfile.gettempdir()
        isinstance(self._ssi, Item)
        eitem = self._ssi.export(
            title=title,
            export_format=export_format,
        )
        save_file = eitem.download(save_path=save_folder)
        eitem.delete(force=True)
        return save_file

    # ----------------------------------------------------------------------
    def generate_report(
        self,
        report_template: Item,
        where: str = "1=1",
        utc_offset: str = "+00:00",
        report_title: Optional[str] = None,
        package_name: Optional[str] = None,
        output_format: str = "docx",
        folder_id: Optional[str] = None,
        merge_files: Optional[str] = None,
        survey_item: Optional[Item] = None,
        webmap_item: Optional[Item] = None,
        map_scale: Optional[float] = None,
        locale: str = "en",
        save_folder: Optional[str] = None,
    ) -> str:
        """
        Creates an MS Word Report or PDF.  The `generate_report` method allows users to either save the
        report to the enterprise or export it directly to disk.

        To save to disk, do not specify a `folder_id`.

        For additional information on parameters, see `Create Report <https://developers.arcgis.com/survey123/api-reference/rest/report/#create-report>`_.

        ================  ===============================================================
        **Parameter**      **Description**
        ----------------  ---------------------------------------------------------------
        report_template   Required :class:`~arcgis.gis.Item` .  The report template Item.
        ----------------  ---------------------------------------------------------------
        where             Optional String. This is the select statement used to export
                          part or whole of the dataset.  If the record count is > 1, then
                          the item must be saved to your organization.
        ----------------  ---------------------------------------------------------------
        utc_offset        Optional String.  This is the time offset from UTC to match the
                          users timezone. Example: EST - "+04:00"
        ----------------  ---------------------------------------------------------------
        report_title      Optional String. Specify the file name (without extension) of the
                          result report file. For example, if outputFormat is .pdf, input:
                          "abc" -> output: "abc.pdf"; input: "abc.docx" -> output: "abc.docx.pdf".

                          If mergeFiles is either nextPage or continuous,
                          outputReportName will be used as the merged file name. See
                          `Create Report <https://developers.arcgis.com/survey123/api-reference/rest/report/#create-report>`_
                          for detailed explanation.
        ----------------  ---------------------------------------------------------------
        package_name      Optional String. Specify the file name (without extension)of the
                          packaged file when packageFiles is true, for example, <outputPackageName>.zip.
        ----------------  ---------------------------------------------------------------
        save_folder       Optional String. Specify the folder location where the output file should be stored.
                          If `folder_id` is specified the save_folder will be ignored.
        ----------------  ---------------------------------------------------------------
        output_format     Optional String. Currently only docx and pdf are supported.
        ----------------  ---------------------------------------------------------------
        folder_id         Optional String. The folder ID of the user's content.
        ----------------  ---------------------------------------------------------------
        merge_files       Optional String. Specify if print multiple records into a single
                          report file (merged mode) or multiple files (split mode), and if
                          in merge mode, start the next record on a new page or continue
                          with the current page. Note: A merged file larger than 500MB
                          will be split into mulitple files.

                          + `none` - Print multiple records in split mode, each record becomes a separated report file. This is the default value.
                          + `nextPage` - Print multiple records in merge mode, the content of the next record starts on the next new page.
                          + `continuous` - Print multiple records in merge mode, the content of the next record starts on the same page of the previous record.
        ----------------  ---------------------------------------------------------------
        survey_item       Optional :class:`~arcgis.gis.Item` . Survey `Item`, to make the operation survey awareness.
        ----------------  ---------------------------------------------------------------
        webmap_item       Optional :class:`~arcgis.gis.Item` . Specify the base map for printing task when printing
                          a point/polyline/polygon. This takes precedence over the map set for
                          each question inside a survey.
        ----------------  ---------------------------------------------------------------
        map_scale         Optional Float. Specify the map scale when printing, the map will center on the feature geometry.
        ----------------  ---------------------------------------------------------------
        locale            Optional String. Specify the locale setting to format number and date values.
        ================  ===============================================================

        :Returns: Item or string upon completion of `Job <https://developers.arcgis.com/survey123/api-reference/rest/report/#jobs>`_.
        For details on the return value, see `Response Parameters <https://developers.arcgis.com/survey123/api-reference/rest/report/#response-parameters>`_
        for :func:`~arcgis.apps.survey123.Survey.generate_report` job.

        """
        if isinstance(where, str):
            where = {"where": where}

        url = "https://{base}/api/featureReport/createReport/submitJob".format(
            base=self._baseurl
        )

        try:
            if (
                self._si._gis.users.me.username == self._si.owner
                and self._ssi_layers[0].properties["isView"] == True
            ):
                fl_url = self.parent_fl_url
            elif self._si._gis.users.me.username != self._si.owner:
                fl_url = self._stk_url
        except KeyError:
            if self._si._gis.users.me.username != self._si.owner:
                fl_url = self._stk_url
            else:
                fl_url = self._ssi_url

        params = {
            "outputFormat": output_format,
            "queryParameters": where,
            "portalUrl": self._si._gis._url,
            "templateItemId": report_template.id,
            "outputReportName": report_title,
            "outputPackageName": package_name,
            "surveyItemId": self._si.id,
            "featureLayerUrl": fl_url,
            "utcOffset": utc_offset,
            "uploadInfo": json.dumps(None),
            "f": "json",
            "username": self._si._gis.users.me.username,
            "locale": locale,
        }
        if merge_files:
            params["mergeFiles"] = merge_files
        if map_scale and isinstance(map_scale, (int, float)):
            params["mapScale"] = map_scale
        if webmap_item and isinstance(webmap_item, Item):
            params["webmapItemId"] = webmap_item.itemid
        if survey_item and isinstance(survey_item, Item):
            params["surveyItemId"] = survey_item.itemid
        if merge_files == "nextPage" or merge_files == "continuous":
            params["package_name"] = ""
        if folder_id:
            params["uploadInfo"] = json.dumps(
                {
                    "type": "arcgis",
                    "packageFiles": True,
                    "parameters": {"folderId": folder_id},
                }
            )
        # 1). Submit the request.
        submit = self._si._gis._con.post(url, params)
        return self._check_status(
            res=submit, status_type="generate_report", save_folder=save_folder
        )

    # ----------------------------------------------------------------------
    @property
    def report_templates(self) -> list:
        """
        Returns a list of saved report items

        :returns: list of :class:`Items <arcgis.gis.Item>`
        """
        related_items = self._si.related_items(
            direction="forward", rel_type="Survey2Data"
        )
        report_templates = [t for t in related_items if t.type == "Microsoft Word"]

        return report_templates

    @property
    def reports(self) -> list:
        """returns a list of generated reports"""
        return self._si._gis.content.search(
            'owner: %s AND type:"Microsoft Word" AND tags:"Survey 123"'
            % self._ssi._gis.users.me.username,
            max_items=10000,
            outside_org=False,
        )

    # ----------------------------------------------------------------------
    def create_report_template(
        self,
        template_type: Optional[str] = "individual",
        template_name: Optional[str] = None,
        save_folder: Optional[str] = None,
    ):
        """
        The `create_report_template` creates a simple default template that
        can be downloaded locally, edited and uploaded back up as a report
        template.

        ================  ===============================================================
        **Parameter**      **Description**
        ----------------  ---------------------------------------------------------------
        template_type     Optional String. Specify which sections to include in the template.
                          Acceptable types are `individual`, `summary`, and `summaryIndividual`.
                          Default is `individual`.
        ----------------  ---------------------------------------------------------------
        template_name     Optional String. Specify the name of the output template file without file extension.
        ----------------  ---------------------------------------------------------------
        save_folder       Optional String. Specify the folder location where the output file should be stored.
        ================  ===============================================================

        :returns: String
        """
        if self._si._gis.users.me.username != self._si.owner:
            raise TypeError("Stakeholders cannot create report templates")
        try:
            if self._ssi_layers[0].properties["isView"] == True:
                fl_url = self.parent_fl_url
        except KeyError:
            fl_url = self._ssi_url

        if template_name:
            file_name = f"{template_name}.docx"
        else:
            if template_type == "individual":
                type = "Individual"
            elif template_type == "summary":
                type = "Summary"
            elif template_type == "summaryIndividual":
                type = "SummaryIndividual"
            file_name = f"{self._si.title}_sampleTemplate{type}.docx"

        url = "https://{base}/api/featureReport/createSampleTemplate".format(
            base=self._baseurl
        )
        gis = self._si._gis
        params = {
            "featureLayerUrl": fl_url,
            "surveyItemId": self._si.id,
            "portalUrl": gis._url,
            "contentType": template_type,
            "username": gis.users.me.username,
            "f": "json",
        }

        res = gis._con.post(
            url,
            params,
            try_json=False,
            out_folder=save_folder,
            file_name=file_name,
        )
        return res

    # ----------------------------------------------------------------------

    def check_template_syntax(self, template_file: Optional[str] = None):
        """
        A sync operation to check any syntax which will lead to a failure
        when generating reports in the given feature.

        ================  ===============================================================
        **Parameter**      **Description**
        ----------------  ---------------------------------------------------------------
        template_file     Required String. The report template file which syntax to be checked.
        ================  ===============================================================

        :returns: dictionary {Success or Failure}
        """

        if self._si._gis.users.me.username != self._si.owner:
            raise TypeError("Stakeholders cannot create report templates")

        try:
            if self._ssi_layers[0].properties["isView"] == True:
                fl_url = self.parent_fl_url
        except KeyError:
            fl_url = self._ssi_url

        url = "https://{base}/api/featureReport/checkTemplateSyntax".format(
            base=self._baseurl
        )
        file = {
            "templateFile": (os.path.basename(template_file), open(template_file, "rb"))
        }
        gis = self._si._gis
        params = {
            "featureLayerUrl": fl_url,
            "surveyItemId": self._si.id,
            "portalUrl": self._si._gis._url,
            "f": "json",
        }

        check = gis._con.post(url, params, files=file)
        return check

    # ----------------------------------------------------------------------

    def upload_report_template(
        self, template_file: Optional[str] = None, template_name: Optional[str] = None
    ):
        """
        Check report template syntax to identify any syntax which will lead to a failure
        when generating reports in the given feature. Uploads the report to the organization
        and associates it with the survey.

        ================  ===============================================================
        **Parameter**      **Description**
        ----------------  ---------------------------------------------------------------
        template_file     Required String. The report template file which syntax to be checked, and uploaded.
        ----------------  ---------------------------------------------------------------
        template_name     Optional String. If provided the resulting item will use the provided name, otherwise
                          the name of the docx file will be used.
        ================  ===============================================================

        :returns: item {Success) or string (Failure}
        """

        check = self.check_template_syntax(template_file)

        if check["success"] == True:
            if template_name:
                file_name = template_name
            else:
                file_name = os.path.splitext(os.path.basename(template_file))[0]

            properties = {
                "title": file_name,
                "type": "Microsoft Word",
                "tags": "Survey123,Print Template,Feature Report Template",
                "typeKeywords": "Survey123,Survey123 Hub,Print Template,Feature Report Template",
                "snippet": "Report template",
            }
            survey_folder_id = self._si.ownerFolder
            gis = self._si._gis
            user = gis.users.get(gis.properties.user.username)
            user_folders = user.folders
            survey_folder = next(
                (f for f in user_folders if f["id"] == survey_folder_id), 0
            )
            folder = survey_folder["title"]
            # folder = "Survey-" + self._si.title
            template_item = gis.content.add(
                item_properties=properties, data=template_file, folder=folder
            )
            add_relationship = self._si.add_relationship(template_item, "Survey2Data")
        else:
            return check["details"][0]["description"]

        return template_item

    # ----------------------------------------------------------------------

    def update_report_template(self, template_file: Optional[str] = None):
        """
        Check report template syntax to identify any syntax which will lead to a failure
        when generating reports in the given feature and updates existing Report template Org item.

        ================  ===============================================================
        **Parameter**      **Description**
        ----------------  ---------------------------------------------------------------
        template_file     Required String. The report template file which syntax to be checked, and uploaded.
                          The updated template name must match the name of the existing template item.
        ================  ===============================================================

        :returns: item {Success) or string (Failure}
        """

        check = self.check_template_syntax(template_file)

        if check["success"] == True:
            file_name = os.path.splitext(os.path.basename(template_file))[0]
            gis = self._si._gis
            template_item = gis.content.search(
                query="title:" + file_name, item_type="Microsoft Word"
            )
            update = template_item[0].update(item_properties={}, data=template_file)
        else:
            return check["details"][0]["description"]

        return template_item

    # ----------------------------------------------------------------------

    def estimate(self, report_template: Item, where: str = "1=1"):
        """
        An operation to estimate how many credits are required for a task
        with the given parameters.

        ================  ===============================================================
        **Parameter**      **Description**
        ----------------  ---------------------------------------------------------------
        report_template   Required :class:`~arcgis.gis.Item` .  The report template Item.
        ----------------  ---------------------------------------------------------------
        where             Optional String. This is the select statement used to export
                          part or whole of the dataset. If the filtered result has more
                          than one feature/record, the request will be considered as a
                          batch printing. Currently, one individual report will be
                          generated for each feature/record.
        ================  ===============================================================

        :returns: dictionary {totalRecords, cost(in credits)}
        """
        try:
            if (
                self._si._gis.users.me.username == self._si.owner
                and self._ssi_layers[0].properties["isView"] == True
            ):
                fl_url = self.parent_fl_url
            elif self._si._gis.users.me.username != self._si.owner:
                fl_url = self._stk_url
        except KeyError:
            if self._si._gis.users.me.username != self._si.owner:
                fl_url = self._stk_url
            else:
                fl_url = self._ssi_url

        gis = self._si._gis
        if isinstance(where, str):
            where = {"where": where}

        url = "https://{base}/api/featureReport/estimateCredits".format(
            base=self._baseurl
        )
        params = {
            "featureLayerUrl": fl_url,
            "queryParameters": where,
            "templateItemId": report_template.id,
            "surveyItemId": self._si.id,
            "portalUrl": self._si._gis._url,
            "f": "json",
        }

        estimate = gis._con.get(url, params)
        return estimate

    # ----------------------------------------------------------------------

    def create_sample_report(
        self,
        report_template: Item,
        where: str = "1=1",
        utc_offset: str = "+00:00",
        report_title: Optional[str] = None,
        merge_files: Optional[str] = None,
        survey_item: Optional[Item] = None,
        webmap_item: Optional[Item] = None,
        map_scale: Optional[float] = None,
        locale: str = "en",
        save_folder: Optional[str] = None,
    ) -> str:
        """
        Similar task to generate_report for creating test sample report, and refining
        a report template before generating any formal report.

        ================  ===============================================================
        **Parameter**      **Description**
        ----------------  ---------------------------------------------------------------
        report_template   Required :class:`~arcgis.gis.Item`  .  The report template Item.
        ----------------  ---------------------------------------------------------------
        where             Optional String. This is the select statement used to export
                          part or whole of the dataset.  If the record count is > 1, then
                          the item must be saved to your organization.
        ----------------  ---------------------------------------------------------------
        utc_offset        Optional String.  This is the time offset from UTC to match the
                          users timezone. Example: EST - "+04:00"
        ----------------  ---------------------------------------------------------------
        report_title      Optional String. Specify the file name (without extension) of the
                          result report file. For example, if outputFormat is .pdf, input:
                          "abc" -> output: "abc.pdf"; input: "abc.docx" -> output: "abc.docx.pdf".

                          If packageFiles is true, outputReportName will be used for report files
                          inside the packaged file. If mergeFiles is either nextPage or continuous,
                          outputReportName will be used as the merged file name.
        ----------------  ---------------------------------------------------------------
        merge_files       Optional String. Specify if print multiple records into a single
                          report file (merged mode) or multiple files (split mode), and if
                          in merge mode, start the next record on a new page or continue
                          with the current page. Note: A merged file larger than 500MB
                          will be split into multiple files.

                          + `none` - Print multiple records in split mode, each record becomes a separated report file. This is the default value.
                          + `nextPage` - Print multiple records in merge mode, the content of the next record starts on the next new page.
                          + `continuous` - Print multiple records in merge mode, the content of the next record starts on the same page of the previous record.
        ----------------  ---------------------------------------------------------------
        save_folder       Optional String. Specify the folder location where the output file should be stored.
        ----------------  ---------------------------------------------------------------
        survey_item       Optional :class:`~arcgis.gis.Item` . Survey `Item`, to make the operation survey awareness.
        ----------------  ---------------------------------------------------------------
        webmap_item       Optional :class:`~arcgis.gis.Item` . Specify the base map for printing task when printing
                          a point/polyline/polygon. This takes precedence over the map set for
                          each question inside a survey.
        ----------------  ---------------------------------------------------------------
        map_scale         Optional Float. Specify the map scale when printing, the map will center on the feature geometry.
        ----------------  ---------------------------------------------------------------
        locale            Optional String. Specify the locale setting to format number and date values.
        ================  ===============================================================

        :Returns: String

        """
        try:
            if (
                self._si._gis.users.me.username == self._si.owner
                and self._ssi_layers[0].properties["isView"] == True
            ):
                fl_url = self.parent_fl_url
            elif self._si._gis.users.me.username != self._si.owner:
                fl_url = self._stk_url
        except KeyError:
            if self._si._gis.users.me.username != self._si.owner:
                fl_url = self._stk_url
            else:
                fl_url = self._ssi_url

        if isinstance(where, str):
            where = {"where": where}

        url = "https://{base}/api/featureReport/createSampleReport/submitJob".format(
            base=self._baseurl
        )

        params = {
            "queryParameters": where,
            "portalUrl": self._si._gis._url,
            "templateItemId": report_template.id,
            "surveyItemId": self._si.id,
            "featureLayerUrl": fl_url,
            "utcOffset": utc_offset,
            "f": "json",
            "locale": locale,
        }
        if merge_files:
            params["mergeFiles"] = merge_files
        if map_scale and isinstance(map_scale, (int, float)):
            params["mapScale"] = map_scale
        if webmap_item and isinstance(webmap_item, Item):
            params["webmapItemId"] = webmap_item.itemid
        if survey_item and isinstance(survey_item, Item):
            params["surveyItemId"] = survey_item.itemid
        if merge_files == "nextPage" or merge_files == "continuous":
            params["package_name"] = ""
        if report_title:
            params["outputReportName"] = report_title

        # 1). Submit the request.
        submit = self._si._gis._con.post(url, params)
        return self._check_status(
            res=submit, status_type="generate_report", save_folder=save_folder
        )

    # ----------------------------------------------------------------------

    def _check_status(self, res, status_type, save_folder):
        """checks the status of a Survey123 operation"""
        jid = res["jobId"]
        gis = self._si._gis
        params = {
            "f": "json",
            "username": self._si._gis.users.me.username,
            "portalUrl": self._si._gis._url,
        }
        status_url = "https://{base}/api/featureReport/jobs/{jid}/status".format(
            base=self._baseurl, jid=jid
        )
        # 3). Start Checking the status
        res = gis._con.get(status_url, params=params)
        while res["jobStatus"] == "esriJobExecuting":
            res = self._si._gis._con.get(status_url, params=params)
            time.sleep(1)
        if status_type == "default_report_template":
            if (
                "results" in res
                and "details" in res["results"]
                and "resultFile" in res["results"]["details"]
                and "url" in res["results"]["details"]["resultFile"]
            ):
                url = res["results"]["details"]["resultFile"]["url"]
                file_name = os.path.basename(url)
                return gis._con.get(url, file_name=file_name, out_folder=save_folder)
            return res
        elif status_type == "generate_report":
            urls = []
            files = []
            items = []
            if res["jobStatus"] == "esriJobSucceeded":
                if "resultFiles" in res["resultInfo"]:
                    for sub in res["resultInfo"]["resultFiles"]:
                        if "id" in sub:
                            items.append(sub["id"])
                        elif "url" in sub:
                            urls.append(sub["url"])
                    files = [
                        self._si._gis._con.get(
                            url,
                            file_name=os.path.basename(urlparse(url).path),
                            add_token=False,
                            try_json=False,
                            out_folder=save_folder,
                        )
                        for url in urls
                    ] + [gis.content.get(i) for i in items]
                    if len(files) == 1:
                        return files[0]
                    return files
                elif "details" in res["resultInfo"]:
                    for res in res["resultInfo"]["details"]:
                        if "resultFile" in res:
                            fr = res["resultFile"]
                            if "id" in fr:
                                items.append(fr["id"])
                            else:
                                urls.append(fr["url"])
                        del res

                    files = [
                        self._si._gis._con.get(
                            url, file_name=os.path.basename(url), out_folder=save_folder
                        )
                        for url in urls
                    ] + [gis.content.get(i) for i in items]
                    if len(files) == 1:
                        return files[0]
                    else:
                        return files
            elif (
                res["jobStatus"] == "esriJobPartialSucceeded"
                or res["jobStatus"] == "esriJobFailed"
            ):
                raise ServerError(res["messages"][0])
            # return

    # ----------------------------------------------------------------------
    def _find_parent(self, view_url):
        """Finds the parent feature layer for a feature layer view"""
        url = view_url + "sources"
        response = self._si._gis._con.get(url)
        return response["services"][0]["url"]

    # ----------------------------------------------------------------------
    def _find_layer_name(self):
        """Finds the name of the layer the survey is submitting to, used to find the appropriate layer index"""
        name = self._si._gis._con.get(
            f"{self._gis._url}/sharing/rest/content/items/{self._si.id}/info/forminfo.json"
        )["name"]
        title = quote(name, safe="()!-_.'~")
        url = f"{self._gis._url}/sharing/rest/content/items/{self._si.id}/info/{title}.xml"
        response = self._si._gis._con.get(url, out_folder=tempfile.gettempdir())
        tree = ET.parse(response)
        root = tree.getroot()
        for elem in root[0][1].iter():
            for key, value in zip(elem.attrib.keys(), elem.attrib.values()):
                if key == "id":
                    return value
