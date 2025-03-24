from mwrogue.esports_client import EsportsClient

site = EsportsClient("lol")

def get_player_image_url(player):
    try:
        response = site.cargo_client.query(
            limit=1,
            tables="PlayerImages=PI, Tournaments=T",
            fields="PI.FileName",
            join_on="PI.Tournament=T.OverviewPage",
            where=f'Link="{player}"',
            order_by="PI.SortDate DESC, T.DateStart DESC"
        )

        if not response:
            return ''

        filename = response[0].get('FileName')
        if not filename:
            return ''

        response = site.client.api(
            action="query",
            format="json",
            titles=f"File:{filename}",
            prop="imageinfo",
            iiprop="url",
            iiurlwidth=None,
        )

        pages = response.get("query", {}).get("pages", {})
        if not pages:
            return ''  # No pages found

        image_info = next(iter(pages.values()), {}).get("imageinfo", [])
        if not image_info:
            return ''  # No image info found

        return image_info[0].get("url", '')

    except Exception as e:
        print(f"Error fetching player image: {e}")
        return ''


def get_image_url(file_name):
    try:
        response = site.client.api(
            action="query",
            format="json",
            titles=f"File:{file_name}",
            prop="imageinfo",
            iiprop="url",
            iiurlwidth=None,
        )

        pages = response.get("query", {}).get("pages", {})
        if not pages:
            return ''  # No pages found

        image_info = next(iter(pages.values()), {}).get("imageinfo", [])
        if not image_info:
            return ''  # No image info found

        return image_info[0].get("url", '')

    except Exception as e:
        print(f"Error fetching team image: {e}")
        return ''

if __name__ == "__main__":
    print("main")