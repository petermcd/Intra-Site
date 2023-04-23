"""Module to handle retrival of product details."""
import abc
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


class ShopInterface(abc.ABC):
    """Interface for shops."""

    @abc.abstractmethod
    def get_product_details(self, url: str) -> ProductDetails:
        """
        Get details regarding a product from shops.

        Args:
            url: URL for the product.

        Returns:
            ProductDetails containing product details.
        """
        raise NotImplementedError


class Amazon(ShopInterface):
    """Class to handle interactions with Amazon."""

    def get_product_details(self, url: str) -> ProductDetails:
        """
        Get details regarding a product from Amazon.

        Args:
            url: URL for the product.

        Returns:
            ProductDetails containing product details.
        """
        fixed_url = url.split(sep="?")[0]
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/112.0.5615.50 Safari/537.36"
            )
        }
        req = requests.get(url=fixed_url, headers=headers)
        if req.status_code != 200:
            raise ProductNotFoundException("Unable to locate product.")
        parsed = BeautifulSoup(req.text, "html.parser")
        name = parsed.title.string
        product_image = ""
        product_image_matches = re.search(r'"hiRes":"([a-zA-Z0-9:\/.+_-]+)"', req.text)
        if product_image_matches:
            product_image = product_image_matches.group(1)
        description = parsed.find("div", {"id": "feature-bullets"}).text
        price = self._normalise_price(
            parsed.find("span", {"id": "sns-base-price"}).contents[0].text
        )
        in_stock = False
        for stock in parsed.find_all("span", {"class": "a-color-attainable"}):
            if "in stock" in stock.text.lower():
                in_stock = True
                break
        product_details = ProductDetails(
            name=name or "",
            product_image=product_image,
            description=description,
            price=int(price),
            product_url=url,
            info_url=url,
            in_stock=in_stock,
        )
        return product_details

    def _normalise_price(self, price: str) -> int:
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


class PiHut(ShopInterface):
    """Class to handle interactions with Pi Hut."""

    def get_product_details(self, url: str) -> ProductDetails:
        """
        Get details regarding a product from PiHut.

        Args:
            url: URL for the product.

        Returns:
            ProductDetails containing product details.
        """
        info_url = f"{url}.js"
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                "(KHTML, like Gecko) Chrome/112.0.5615.50 Safari/537.36"
            )
        }
        req = requests.get(url=info_url, headers=headers)
        if req.status_code != 200:
            raise ProductNotFoundException("Unable to locate product.")
        data = req.json()
        product_details = ProductDetails(
            name=data["title"],
            product_image=data["media"][0]["src"],
            description=data["description"],
            price=int(data["price"]),
            product_url=url,
            info_url=info_url,
            in_stock=data["available"],
        )
        return product_details


class Ikea(ShopInterface):
    """Class to handle interactions with Ikea."""

    def get_product_details(self, url: str) -> ProductDetails:
        """
        Get details regarding a product from Ikea.

        Args:
            url: URL for the product.

        Returns:
            ProductDetails containing product details.
        """
        fixed_url = url.split(sep="?")[0]
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/112.0.5615.50 Safari/537.36"
            )
        }
        req = requests.get(url=fixed_url, headers=headers)
        if req.status_code != 200:
            raise ProductNotFoundException("Unable to locate product.")
        parsed = BeautifulSoup(req.text, "html.parser")
        name = parsed.title.string
        product_image = parsed.find("img", {"class": "pip-image"}).attrs["src"]
        description = parsed.find("p", {"class": "pip-product-details__paragraph"}).text
        price = self._normalise_price(
            parsed.find("span", {"class": "pip-temp-price__integer"}).text
        )
        in_stock = False
        product_details = ProductDetails(
            name=name or "",
            product_image=product_image,
            description=description,
            price=int(price),
            product_url=url,
            info_url=url,
            in_stock=in_stock,
        )
        return product_details

    def _normalise_price(self, price: str) -> int:
        """
        Convert a price as a string to an int.

        Args:
            price: Price as a string.

        Returns:
            Price as an int in pence.
        """
        price = price.strip()
        return int(float(price) * 100)


class Unknown(ShopInterface):
    """Class to handle interactions with unknown sites."""

    def get_product_details(self, url: str) -> ProductDetails:
        """
        Get details regarding a product from Unknown sellers.

        Args:
            url: URL for the product.

        Returns:
            ProductDetails containing product details.
        """
        fixed_url = url.split(sep="?")[0]
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/112.0.5615.50 Safari/537.36"
            )
        }
        req = requests.get(url=fixed_url, headers=headers)
        if req.status_code != 200:
            raise ProductNotFoundException("Unable to locate product.")
        parsed = BeautifulSoup(req.text, "html.parser")
        name = parsed.title.string
        description = "UNKNOWN"
        price = 0
        in_stock = False
        product_details = ProductDetails(
            name=name or "",
            product_image="",
            description=description,
            price=int(price),
            product_url=url,
            info_url=url,
            in_stock=in_stock,
        )
        return product_details


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

    def shop(self, url: str) -> ShopInterface:
        """
        Provide the shop object.

        Args:
            url: The name of the required shop.

        Returns:
            ShopInterface object.
        """
        for store_url in SHOP_MAP.keys():
            if url.lower().startswith(store_url):
                shop_obj = SHOP_MAP[store_url]()  # type: ignore
                return shop_obj
        return Unknown()
