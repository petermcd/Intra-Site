"""Module to handle retrival of product details."""
import abc
import json
import re
from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup


@dataclass
class ProductDetails:
    """Data class for storing product details."""

    name: str
    product_image: str
    description: str
    price: int
    product_url: str
    info_url: str
    in_stock: bool


class ProductNotFoundException(Exception):
    """Exception to handle a product not being found."""

    pass


class Shop(metaclass=abc.ABCMeta):
    """Interface for shops."""

    __slots__ = ("_response", "_url")

    def __init__(self, url: str):
        """
        Initialise Shop.

        Args:
            url: Product URL.
        """
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/112.0.5615.50 Safari/537.36"
            )
        }
        self._response = requests.get(url=url, headers=headers)
        if self._response.status_code != 200:
            raise ProductNotFoundException("Unable to locate product.")
        self._url = url

    @abc.abstractmethod
    def get_product_details(self) -> ProductDetails:
        """
        Get details regarding a product from shops.

        Returns:
            ProductDetails containing product details.
        """
        raise NotImplementedError

    @staticmethod
    def normalise_price_from_float(price: float) -> int:
        """
        Convert a price as a string to an int.

        Args:
            price: Price as a string.

        Returns:
            Price as an int in pence.
        """
        return int(price * 100)

    @staticmethod
    def normalise_price(price: str) -> int:
        """
        Convert a price as a string to an int.

        Args:
            price: Price as a string.

        Returns:
            Price as an int in pence.
        """
        price = price.strip()
        price = price[1:]
        return int(float(price) * 100)


class Amazon(Shop):
    """Class to handle interactions with Amazon."""

    def __init__(self, url: str):
        """
        Initialise Amazon.

        Args:
            url: Product URL.
        """
        fixed_url = url.split(sep="?")[0]
        super().__init__(url=fixed_url)

    def get_product_details(self) -> ProductDetails:
        """
        Get details regarding a product from Amazon.

        Returns:
            ProductDetails containing product details.
        """
        parsed = BeautifulSoup(self._response.text, "html.parser")
        name = parsed.title.string
        return ProductDetails(
            name=name or "",
            product_image=self._get_product_image(parsed_data=parsed),
            description=self._get_description(parsed_data=parsed),
            price=self._get_price(parsed_data=parsed),
            product_url=self._url,
            info_url=self._url,
            in_stock=self._get_stock_availability(parsed_data=parsed),
        )

    @staticmethod
    def _get_description(parsed_data) -> str:
        """
        Identify the description of the product.

        Args:
            parsed_data: Source of the product page as parsed by BeatifulSoup

        Returns:
             Product description.
        """
        if description_search := parsed_data.find(
            "div", {"class": "a-expander-partial-collapse-content"}
        ):
            return description_search.text
        description = "UNKNOWN"
        return (
            description_search.text
            if (
                description_search := parsed_data.find("div", {"id": "feature-bullets"})
            )
            else description
        )

    def _get_price(self, parsed_data) -> int:
        """
        Identify the price of the product.

        Args:
            parsed_data: Source of the product page as parsed by BeatifulSoup

        Returns:
             Price as an int
        """
        return (
            self.normalise_price(price_search.text)
            if (
                price_search := parsed_data.find("span", {"class": "a-price"}).contents[
                    0
                ]
            )
            else 0
        )

    def _get_product_image(self, parsed_data) -> str:
        """
        Identify the product image.

        Args:
            parsed_data: Source of the product page as parsed by BeatifulSoup.

        Returns:
             Product image URL or an empty string.
        """
        if product_image_matches := parsed_data.find("img", {"id": "imgBlkFront"}):
            product_image_field = product_image_matches.attrs["data-a-dynamic-image"]
            product_image_json = json.loads(product_image_field)
            return list(product_image_json.keys())[0]
        if product_image_matches := re.search(
            r'"hiRes":"([a-zA-Z0-9:/.+_-]+)"', self._response.text
        ):
            return product_image_matches[1]
        else:
            return ""

    @staticmethod
    def _get_stock_availability(parsed_data) -> bool:
        """
        Identify if the product is in stock.

        Args:
            parsed_data: Source of the product page as parsed by BeatifulSoup

        Returns:
             True if in stock otherwise False
        """
        for stock in parsed_data.find_all("span", {"class": "a-color-attainable"}):
            if "in stock" in stock.text.lower():
                return True
        return any(
            "in stock" in stock.text.lower()
            for stock in parsed_data.find_all("span", {"class": "a-color-success"})
        )


class Ikea(Shop):
    """Class to handle interactions with Ikea."""

    def __init__(self, url: str):
        """
        Initialise Ikea.

        Args:
            url: Product URL.
        """
        fixed_url = url.split(sep="?")[0]
        super().__init__(url=fixed_url)

    def get_product_details(self) -> ProductDetails:
        """
        Get details regarding a product from Ikea.

        Returns:
            ProductDetails containing product details.
        """
        parsed = BeautifulSoup(self._response.text, "html.parser")
        name = parsed.title.string
        product_image = parsed.find("img", {"class": "pip-image"}).attrs["src"]
        description = parsed.find("p", {"class": "pip-product-details__paragraph"}).text
        price = self.normalise_price_from_float(
            float(parsed.find("span", {"class": "pip-temp-price__integer"}).text)
        )
        in_stock = False
        return ProductDetails(
            name=name or "",
            product_image=product_image,
            description=description,
            price=int(price),
            product_url=self._url,
            info_url=self._url,
            in_stock=in_stock,
        )


class PiHut(Shop):
    """Class to handle interactions with Pi Hut."""

    __slots__ = (
        "_product_url",
        "_response",
    )

    def __init__(self, url: str):
        """
        Initialise PiHut.

        Args:
            url: Product URL.
        """
        info_url = f"{url}.js"
        self._product_url = url
        super().__init__(url=info_url)

    def get_product_details(self) -> ProductDetails:
        """
        Get details regarding a product from PiHut.

        Returns:
            ProductDetails containing product details.
        """
        data = self._response.json()
        return ProductDetails(
            name=data["title"],
            product_image=data["media"][0]["src"],
            description=data["description"],
            price=int(data["price"]),
            product_url=self._product_url,
            info_url=self._url,
            in_stock=data["available"],
        )


class Unknown(Shop):
    """Class to handle interactions with unknown sites."""

    def __init__(self, url: str):
        """
        Initialise Unknown.

        Args:
            url: Product URL.
        """
        fixed_url = url.split(sep="?")[0]
        super().__init__(url=fixed_url)

    def get_product_details(self) -> ProductDetails:
        """
        Get details regarding a product from Unknown sellers.

        Returns:
            ProductDetails containing product details.
        """
        parsed = BeautifulSoup(self._response.text, "html.parser")
        name = parsed.title.string
        description = "UNKNOWN"
        price = 0
        in_stock = False
        return ProductDetails(
            name=name or "",
            product_image="",
            description=description,
            price=price,
            product_url=self._url,
            info_url=self._url,
            in_stock=in_stock,
        )


SHOP_MAP = {
    "https://thepihut.com/": PiHut,
    "https://www.thepihut.com/": PiHut,
    "https://www.amazon": Amazon,
    "https://amazon": Amazon,
    "https://ikea.com": Ikea,
    "https://www.ikea.com": Ikea,
}


class ProductDetailsFactory:
    """Factory to provide the correct shop object."""

    @staticmethod
    def shop(url: str) -> Shop:
        """
        Provide the shop object.

        Args:
            url: The name of the required shop.

        Returns:
            ShopInterface object.
        """
        for store_url in SHOP_MAP.keys():
            if url.lower().startswith(store_url):
                return SHOP_MAP[store_url](url=url)  # type: ignore
        return Unknown(url=url)
