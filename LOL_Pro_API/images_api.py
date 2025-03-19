from mwrogue.esports_client import EsportsClient


def get_player_image_url(player, width=None):
    try:
        site = EsportsClient("lol")
        response = site.cargo_client.query(
            limit=1,
            tables="PlayerImages=PI, Tournaments=T",
            fields="PI.FileName",
            join_on="PI.Tournament=T.OverviewPage",
            where='Link="%s"' % player,
            order_by="PI.SortDate DESC, T.DateStart DESC"
        )

        filename = response[0]['FileName']

        response = site.client.api(
            action="query",
            format="json",
            titles=f"File:{filename}",
            prop="imageinfo",
            iiprop="url",
            iiurlwidth=width,
        )

        image_info = next(iter(response["query"]["pages"].values()))["imageinfo"][0]

        if width:
            url = image_info["thumburl"]
        else:
            url = image_info["url"]
        return url
    except Exception:
        return ''