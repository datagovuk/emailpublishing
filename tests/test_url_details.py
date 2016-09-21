

from emailpub.common import details_from_link


def test_guessing():
    n, t = details_from_link("https://gov.uk")
    assert t == "UNKNOWN"
    assert n == "Resource"

    n, t = details_from_link("https://www.gov.uk/government/uploads/system/uploads/attachment_data/file/447348/20150629_HoC_Report_Jun15.csv")
    assert t == "CSV"
    assert n == "20150629 HoC Report Jun15"

    n, t = details_from_link("https://www.gov.uk/government/uploads/system/uploads/attachment_data/file/447348/20150629_HoC_Report_Jun15")
    assert t == "UNKNOWN"
    assert n == "20150629 HoC Report Jun15"