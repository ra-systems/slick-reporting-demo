from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.template.defaultfilters import date
from django.views.generic import TemplateView
from slick_reporting.views import SlickReportViewBase, SlickReportView as OriginalReportView
from slick_reporting.fields import SlickReportField
from .models import SalesLineTransaction
from django.utils.translation import ugettext_lazy as _
import inspect

User = get_user_model()


class GroupByViewWith2ChartsRaw(OriginalReportView):
    """
    We can have multiple charts, and multiple Calculation fields
    """

    report_model = SalesLineTransaction
    date_field = 'transaction_date'
    group_by = 'product'
    columns = ['name',
               SlickReportField.create(Sum, 'quantity', name='quantity__sum', verbose_name=_('Quantities Sold')),
               SlickReportField.create(Sum, 'value', name='value__sum', verbose_name=_('Value $')),
               ]

    chart_settings = [
        {'type': 'pie',
         'engine_name': 'highcharts',
         'data_source': ['quantity__sum'],
         'title_source': ['name'],
         'title': 'Pie Chart (Quantities) Highcharts'
         },
        {'type': 'pie',
         'engine_name': 'chartsjs',
         'data_source': ['quantity__sum'],
         'title_source': ['name'],
         'title': 'Pie Chart (Quantities) ChartsJs'
         },
        {'type': 'bar',
         'engine_name': 'highcharts',
         'data_source': ['value__sum'],
         'title_source': ['name'],
         'title': 'Column Chart (Values)'
         },
        {'type': 'bar',
         'engine_name': 'chartsjs',
         'data_source': ['value__sum'],
         'title_source': ['name'],
         'title': 'Column Chart (Values)'
         },
    ]


class Index(TemplateView):
    template_name = 'slick_example/index.html'


class SlickReportView(SlickReportViewBase):
    # template_name = 'slick_example/simple_report.html'
    code = ''
    comment = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['code'] = inspect.getsource(self.__class__)
        # context['code'] = highlight(inspect.getsource(self.__class__), PythonLexer(), HtmlFormatter(style='colorful'))
        context['code'] = inspect.getsource(self.__class__)
        # context['comment'] = publish_parts(self.comment, writer_name='html')['html_body']
        # context['comment'] = publish_parts(self.__class__.__doc__ or '', writer_name='html')['html_body']

        code = 'print "Hello World"'
        # print()

        return context


class SimpleListReport(SlickReportView):
    """
    Let's start by simply creating a page where we can filter our report_model record / dataset.
    In this example we inherit from The class `SlickReportView` (which is CBV in essence).

    Mandatory configuration for a ``SlickReportView`` are:
    `report_model` is the django model that contains the data we're interested in computing over.
    `date_field` a Date/DateTime field on the report model to be used for filtering and computing.
    `columns`:   a list of 1. fields on the report model or 2.SlickReportField names or classes.

    """

    report_model = SalesLineTransaction
    date_field = 'transaction_date'

    columns = ['transaction_date', 'client', 'product', 'quantity', 'price', 'value']


class NoGroupByPlusChart(SlickReportView):
    """
    Let's explore more capabilities to the SlickReportView.

    Instead of showing the Client and Product id, like previous example, we will show their names and enhance how the date is displayed
    """

    report_model = SalesLineTransaction
    date_field = 'transaction_date'
    columns = ['transaction_date', 'client__name', 'product__name', 'quantity', 'price', 'value']

    def format_row(self, row_obj):
        """
        A hook to format each row . This method gets called on each row in the results.
        :param row_obj: a dict representing a single row in the results
        :return: A dict representing a single row in the results
        """

        row_obj['transaction_date'] = date(row_obj['transaction_date'], 'd-m-y H:i')
        return row_obj


class GroupByIntro(SlickReportView):
    """
    We start doing more interesting stuff by aggregating and computing values for groups of data in our report model.

    Here we group by the `product` ForeignKey and compute the sum of the `value` field in
    our report_model `SalesLineTransaction`.. giving us the sale worth for each product.
    """

    report_model = SalesLineTransaction
    date_field = 'transaction_date'
    group_by = 'product'
    columns = ['name',
               SlickReportField.create(Sum, 'value', name='value__sum', verbose_name=_('Total sold $')),
               ]


class GroupByView(SlickReportView):
    """
    It's easy to add chart(s) to the view, using `chart_settings` which is a list of object, each object represent a chart

    Chart Object
    * type: what kind of chart it is bar, pie, line, column
    * data_source: a list of Field name(s) of containing the numbers we want to chart,
    * title_source: a list label(s) respective to the `data_source`.

    * title: (optional) The chart title
    * id: (optional) Name used to refer to this exact chart in front end default is `type-{index}`
    """

    report_model = SalesLineTransaction
    date_field = 'transaction_date'
    group_by = 'product'
    columns = ['name',
               SlickReportField.create(Sum, 'quantity', name='quantity__sum', verbose_name=_('Quantities Sold')),
               ]

    chart_settings = [{
        'type': 'pie',
        'data_source': ['quantity__sum'],
        'title_source': ['name'],
    }]


class GroupByViewWith2Charts(SlickReportView):
    """
    We can have multiple charts, multiple Calculation fields and multiple charting engines !!
    Slick Reporting by default comes with 2 charting engine support `Highcharts` and `ChartsJs`
    You can set the engine_name per chart, if not set it defaults to ``SLICK_REPORTING_DEFAULT_CHARTS_ENGINE``
    """

    report_model = SalesLineTransaction
    date_field = 'transaction_date'
    group_by = 'product'
    columns = ['name',
               SlickReportField.create(Sum, 'quantity', name='quantity__sum', verbose_name=_('Quantities Sold')),
               SlickReportField.create(Sum, 'value', name='value__sum', verbose_name=_('Value $')),
               ]

    chart_settings = [
        {'type': 'pie',
         'engine_name': 'highcharts', # setting the engine per chart
         'data_source': ['quantity__sum'],
         'title_source': ['name'],
         'title': 'Pie Chart (Quantities) Highcharts'
         },
        {'type': 'pie',
         'engine_name': 'chartsjs',  # setting the engine per chart
         'data_source': ['quantity__sum'],
         'title_source': ['name'],
         'title': 'Pie Chart (Quantities) ChartsJs'
         },

        # no engine_name set, fall back to the default set in SLICK_REPORTING_DEFAULT_CHARTS_ENGINE
        {'type': 'bar',
         'data_source': ['value__sum'],
         'title_source': ['name'],
         'title': 'Column Chart (Values)'
         },
    ]


class TimeSeries(SlickReportView):
    """
    A time series is a series of data points indexed in time order. Most commonly, a time series is a sequence taken at
    successive equally spaced points in time. - from Wikipedia


    `time_series_pattern` Possible options are: daily, weekly, semimonthly, monthly, quarterly, semiannually, annually and custom.
    `time_series_columns` A list of SlickReportField classes (or names registered) , which will  be computed for each series.

    In this example we can see how many pieces of each product were sold each month.
    """

    report_model = SalesLineTransaction
    date_field = 'transaction_date'
    group_by = 'product'
    columns = ['name']

    # To activate a time series we need to set
    time_series_pattern = 'monthly'
    time_series_columns = [
        SlickReportField.create(Sum, 'quantity', name='quantity__sum', verbose_name=_('Quantities Sold'))
    ]


class TimeSeriesCustomization(SlickReportView):
    """
    Let's explore more options by SlickReportView.

    1.  the `'__time_series__' special column name used to control the placing of the time series columns inside your columns.
        Default behavior is to add he time series columns at the end of the columns
    2. Plot charts, note that here we can use `plot_total` to plot the total of the time series instead of the details
    """

    report_model = SalesLineTransaction
    date_field = 'transaction_date'
    group_by = 'product'
    columns = ['name',
               '__time_series__',
               SlickReportField.create(Sum, 'value', name='value__sum', verbose_name=_('Grand Sum')),
               ]

    time_series_pattern = 'monthly'
    time_series_columns = [
        SlickReportField.create(Sum, 'value', name='value__sum', verbose_name=_('Sum per month'))
    ]

    chart_settings = [
        {'type': 'bar',
         'data_source': ['value__sum'],
         'title_source': ['name'],
         'title': 'Quantities per product per month'
         },
        {'type': 'bar',
         'data_source': ['value__sum'],
         'title_source': ['name'],
         'title': 'Total quantities per month',
         'plot_total': True  # plot total instead of the details
         },
    ]


class CrossTabReportView(SlickReportView):
    """
    Crosstab reports, also known as matrix reports, to show the relationships between three or more query items.
    Crosstab reports show data in rows and columns with information summarized at the intersection points.

    To get a better idea on what this report does please choose a client -or more- and check the results.
    """

    report_model = SalesLineTransaction
    date_field = 'transaction_date'

    group_by = 'product'
    columns = ['slug', 'name']

    # To activate Crosstab
    crosstab_model = 'client'
    crosstab_columns = [SlickReportField.create(Sum, 'value', name='value__sum', verbose_name=_('Sales'))]


class CrosstabCustomization(SlickReportView):
    """
    Let's add some charts and customizations
    Like time series, the special column name `__crosstab__` is used to place the crosstab columns inside your columns.
    In this example you can see the crosstab columns are in the left most of the columns. 

    `crosstab_compute_reminder` is responsible for adding that last column in the crosstab called `Reminder` to compute
    on all entities except those which were chosen.
    
    chart_settings.plot_total also works here.

    """
    report_model = SalesLineTransaction
    report_title = _('Product Client sales Cross-tab')
    date_field = 'transaction_date'

    group_by = 'product'
    columns = ['__crosstab__', 'slug', 'name']

    crosstab_model = 'client'
    crosstab_columns = [SlickReportField.create(Sum, 'value', name='value__sum', verbose_name=_('Sales'))]
    crosstab_compute_reminder = True

    chart_settings = [
        {
            'type': 'bar',
            'data_source': ['value__sum'],
            'title_source': ['name'],
            'title': _('Per Client Per Product'),

        },
        {
            'type': 'bar',
            'data_source': ['value__sum'],
            'plot_total': True,
            'title_source': ['name'],
            'stacking': 'normal',
            'title': _('Per Client Total'),

        },
        {
            'type': 'pie',
            'data_source': ['value__sum'],
            'plot_total': True,
            'title_source': ['name'],
            'title': _('Per Client Total %'),

        }
    ]


class LogIns(SlickReportView):
    """
    We can group by date
    In this example, we can count how many user joined each day.
    """

    report_model = User
    date_field = 'date_joined'
    group_by = 'date_joined'
    columns = ['date_joined', 'count__logins']

    chart_settings = [{
        'type': 'bar',
        'data_source': ['count__logins'],
        'title_source': 'date_joined',
        'title': 'Logins Per Day'
    }, ]
