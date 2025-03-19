from mwrogue.esports_client import EsportsClient

site = EsportsClient("lol")

def get_player_image_url(player):
    try:
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
            iiurlwidth=None,
        )

        image_info = next(iter(response["query"]["pages"].values()))["imageinfo"][0]

        return image_info["url"]
    except Exception:
        return ''



def get_team_image_url(team):
    response = site.client.api(
        action="query",
        format="json",
        titles=f"File:{team}logo square.png",
        prop="imageinfo",
        iiprop="url",
        iiurlwidth=None,
    )

    image_info = next(iter(response["query"]["pages"].values()))["imageinfo"][0]

    return image_info["url"]

