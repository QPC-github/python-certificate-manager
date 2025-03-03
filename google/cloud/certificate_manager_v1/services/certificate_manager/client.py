# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from collections import OrderedDict
import os
import re
from typing import (
    Dict,
    Mapping,
    MutableMapping,
    MutableSequence,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
    cast,
)

from google.api_core import client_options as client_options_lib
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.exceptions import MutualTLSChannelError  # type: ignore
from google.auth.transport import mtls  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.certificate_manager_v1 import gapic_version as package_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore

from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.longrunning import operations_pb2
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore

from google.cloud.certificate_manager_v1.services.certificate_manager import pagers
from google.cloud.certificate_manager_v1.types import certificate_issuance_config
from google.cloud.certificate_manager_v1.types import (
    certificate_issuance_config as gcc_certificate_issuance_config,
)
from google.cloud.certificate_manager_v1.types import certificate_manager

from .transports.base import DEFAULT_CLIENT_INFO, CertificateManagerTransport
from .transports.grpc import CertificateManagerGrpcTransport
from .transports.grpc_asyncio import CertificateManagerGrpcAsyncIOTransport


class CertificateManagerClientMeta(type):
    """Metaclass for the CertificateManager client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = (
        OrderedDict()
    )  # type: Dict[str, Type[CertificateManagerTransport]]
    _transport_registry["grpc"] = CertificateManagerGrpcTransport
    _transport_registry["grpc_asyncio"] = CertificateManagerGrpcAsyncIOTransport

    def get_transport_class(
        cls,
        label: Optional[str] = None,
    ) -> Type[CertificateManagerTransport]:
        """Returns an appropriate transport class.

        Args:
            label: The name of the desired transport. If none is
                provided, then the first transport in the registry is used.

        Returns:
            The transport class to use.
        """
        # If a specific transport is requested, return that one.
        if label:
            return cls._transport_registry[label]

        # No transport is requested; return the default (that is, the first one
        # in the dictionary).
        return next(iter(cls._transport_registry.values()))


class CertificateManagerClient(metaclass=CertificateManagerClientMeta):
    """API Overview

    Certificates Manager API allows customers to see and manage all
    their TLS certificates.

    Certificates Manager API service provides methods to manage
    certificates, group them into collections, and create serving
    configuration that can be easily applied to other Cloud resources
    e.g. Target Proxies.

    Data Model

    The Certificates Manager service exposes the following resources:

    -  ``Certificate`` which describes a single TLS certificate.
    -  ``CertificateMap`` which describes a collection of certificates
       that can be attached to a target resource.
    -  ``CertificateMapEntry`` which describes a single configuration
       entry that consists of a SNI and a group of certificates. It's a
       subresource of CertificateMap.

    Certificate, CertificateMap and CertificateMapEntry IDs have to
    match "^[a-z0-9-]{1,63}$" regexp, which means that

    -  only lower case letters, digits, and hyphen are allowed
    -  length of the resource ID has to be in [1,63] range.

    Provides methods to manage Cloud Certificate Manager entities.
    """

    @staticmethod
    def _get_default_mtls_endpoint(api_endpoint):
        """Converts api endpoint to mTLS endpoint.

        Convert "*.sandbox.googleapis.com" and "*.googleapis.com" to
        "*.mtls.sandbox.googleapis.com" and "*.mtls.googleapis.com" respectively.
        Args:
            api_endpoint (Optional[str]): the api endpoint to convert.
        Returns:
            str: converted mTLS api endpoint.
        """
        if not api_endpoint:
            return api_endpoint

        mtls_endpoint_re = re.compile(
            r"(?P<name>[^.]+)(?P<mtls>\.mtls)?(?P<sandbox>\.sandbox)?(?P<googledomain>\.googleapis\.com)?"
        )

        m = mtls_endpoint_re.match(api_endpoint)
        name, mtls, sandbox, googledomain = m.groups()
        if mtls or not googledomain:
            return api_endpoint

        if sandbox:
            return api_endpoint.replace(
                "sandbox.googleapis.com", "mtls.sandbox.googleapis.com"
            )

        return api_endpoint.replace(".googleapis.com", ".mtls.googleapis.com")

    DEFAULT_ENDPOINT = "certificatemanager.googleapis.com"
    DEFAULT_MTLS_ENDPOINT = _get_default_mtls_endpoint.__func__(  # type: ignore
        DEFAULT_ENDPOINT
    )

    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            CertificateManagerClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_info(info)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    @classmethod
    def from_service_account_file(cls, filename: str, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            CertificateManagerClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> CertificateManagerTransport:
        """Returns the transport used by the client instance.

        Returns:
            CertificateManagerTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def ca_pool_path(
        project: str,
        location: str,
        ca_pool: str,
    ) -> str:
        """Returns a fully-qualified ca_pool string."""
        return "projects/{project}/locations/{location}/caPools/{ca_pool}".format(
            project=project,
            location=location,
            ca_pool=ca_pool,
        )

    @staticmethod
    def parse_ca_pool_path(path: str) -> Dict[str, str]:
        """Parses a ca_pool path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/caPools/(?P<ca_pool>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def certificate_path(
        project: str,
        location: str,
        certificate: str,
    ) -> str:
        """Returns a fully-qualified certificate string."""
        return (
            "projects/{project}/locations/{location}/certificates/{certificate}".format(
                project=project,
                location=location,
                certificate=certificate,
            )
        )

    @staticmethod
    def parse_certificate_path(path: str) -> Dict[str, str]:
        """Parses a certificate path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/certificates/(?P<certificate>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def certificate_issuance_config_path(
        project: str,
        location: str,
        certificate_issuance_config: str,
    ) -> str:
        """Returns a fully-qualified certificate_issuance_config string."""
        return "projects/{project}/locations/{location}/certificateIssuanceConfigs/{certificate_issuance_config}".format(
            project=project,
            location=location,
            certificate_issuance_config=certificate_issuance_config,
        )

    @staticmethod
    def parse_certificate_issuance_config_path(path: str) -> Dict[str, str]:
        """Parses a certificate_issuance_config path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/certificateIssuanceConfigs/(?P<certificate_issuance_config>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def certificate_map_path(
        project: str,
        location: str,
        certificate_map: str,
    ) -> str:
        """Returns a fully-qualified certificate_map string."""
        return "projects/{project}/locations/{location}/certificateMaps/{certificate_map}".format(
            project=project,
            location=location,
            certificate_map=certificate_map,
        )

    @staticmethod
    def parse_certificate_map_path(path: str) -> Dict[str, str]:
        """Parses a certificate_map path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/certificateMaps/(?P<certificate_map>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def certificate_map_entry_path(
        project: str,
        location: str,
        certificate_map: str,
        certificate_map_entry: str,
    ) -> str:
        """Returns a fully-qualified certificate_map_entry string."""
        return "projects/{project}/locations/{location}/certificateMaps/{certificate_map}/certificateMapEntries/{certificate_map_entry}".format(
            project=project,
            location=location,
            certificate_map=certificate_map,
            certificate_map_entry=certificate_map_entry,
        )

    @staticmethod
    def parse_certificate_map_entry_path(path: str) -> Dict[str, str]:
        """Parses a certificate_map_entry path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/certificateMaps/(?P<certificate_map>.+?)/certificateMapEntries/(?P<certificate_map_entry>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def dns_authorization_path(
        project: str,
        location: str,
        dns_authorization: str,
    ) -> str:
        """Returns a fully-qualified dns_authorization string."""
        return "projects/{project}/locations/{location}/dnsAuthorizations/{dns_authorization}".format(
            project=project,
            location=location,
            dns_authorization=dns_authorization,
        )

    @staticmethod
    def parse_dns_authorization_path(path: str) -> Dict[str, str]:
        """Parses a dns_authorization path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/dnsAuthorizations/(?P<dns_authorization>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def common_billing_account_path(
        billing_account: str,
    ) -> str:
        """Returns a fully-qualified billing_account string."""
        return "billingAccounts/{billing_account}".format(
            billing_account=billing_account,
        )

    @staticmethod
    def parse_common_billing_account_path(path: str) -> Dict[str, str]:
        """Parse a billing_account path into its component segments."""
        m = re.match(r"^billingAccounts/(?P<billing_account>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_folder_path(
        folder: str,
    ) -> str:
        """Returns a fully-qualified folder string."""
        return "folders/{folder}".format(
            folder=folder,
        )

    @staticmethod
    def parse_common_folder_path(path: str) -> Dict[str, str]:
        """Parse a folder path into its component segments."""
        m = re.match(r"^folders/(?P<folder>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_organization_path(
        organization: str,
    ) -> str:
        """Returns a fully-qualified organization string."""
        return "organizations/{organization}".format(
            organization=organization,
        )

    @staticmethod
    def parse_common_organization_path(path: str) -> Dict[str, str]:
        """Parse a organization path into its component segments."""
        m = re.match(r"^organizations/(?P<organization>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_project_path(
        project: str,
    ) -> str:
        """Returns a fully-qualified project string."""
        return "projects/{project}".format(
            project=project,
        )

    @staticmethod
    def parse_common_project_path(path: str) -> Dict[str, str]:
        """Parse a project path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_location_path(
        project: str,
        location: str,
    ) -> str:
        """Returns a fully-qualified location string."""
        return "projects/{project}/locations/{location}".format(
            project=project,
            location=location,
        )

    @staticmethod
    def parse_common_location_path(path: str) -> Dict[str, str]:
        """Parse a location path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)$", path)
        return m.groupdict() if m else {}

    @classmethod
    def get_mtls_endpoint_and_cert_source(
        cls, client_options: Optional[client_options_lib.ClientOptions] = None
    ):
        """Return the API endpoint and client cert source for mutual TLS.

        The client cert source is determined in the following order:
        (1) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is not "true", the
        client cert source is None.
        (2) if `client_options.client_cert_source` is provided, use the provided one; if the
        default client cert source exists, use the default one; otherwise the client cert
        source is None.

        The API endpoint is determined in the following order:
        (1) if `client_options.api_endpoint` if provided, use the provided one.
        (2) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is "always", use the
        default mTLS endpoint; if the environment variabel is "never", use the default API
        endpoint; otherwise if client cert source exists, use the default mTLS endpoint, otherwise
        use the default API endpoint.

        More details can be found at https://google.aip.dev/auth/4114.

        Args:
            client_options (google.api_core.client_options.ClientOptions): Custom options for the
                client. Only the `api_endpoint` and `client_cert_source` properties may be used
                in this method.

        Returns:
            Tuple[str, Callable[[], Tuple[bytes, bytes]]]: returns the API endpoint and the
                client cert source to use.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If any errors happen.
        """
        if client_options is None:
            client_options = client_options_lib.ClientOptions()
        use_client_cert = os.getenv("GOOGLE_API_USE_CLIENT_CERTIFICATE", "false")
        use_mtls_endpoint = os.getenv("GOOGLE_API_USE_MTLS_ENDPOINT", "auto")
        if use_client_cert not in ("true", "false"):
            raise ValueError(
                "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
            )
        if use_mtls_endpoint not in ("auto", "never", "always"):
            raise MutualTLSChannelError(
                "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
            )

        # Figure out the client cert source to use.
        client_cert_source = None
        if use_client_cert == "true":
            if client_options.client_cert_source:
                client_cert_source = client_options.client_cert_source
            elif mtls.has_default_client_cert_source():
                client_cert_source = mtls.default_client_cert_source()

        # Figure out which api endpoint to use.
        if client_options.api_endpoint is not None:
            api_endpoint = client_options.api_endpoint
        elif use_mtls_endpoint == "always" or (
            use_mtls_endpoint == "auto" and client_cert_source
        ):
            api_endpoint = cls.DEFAULT_MTLS_ENDPOINT
        else:
            api_endpoint = cls.DEFAULT_ENDPOINT

        return api_endpoint, client_cert_source

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Optional[Union[str, CertificateManagerTransport]] = None,
        client_options: Optional[Union[client_options_lib.ClientOptions, dict]] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the certificate manager client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, CertificateManagerTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (Optional[Union[google.api_core.client_options.ClientOptions, dict]]): Custom options for the
                client. It won't take effect if a ``transport`` instance is provided.
                (1) The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client. GOOGLE_API_USE_MTLS_ENDPOINT
                environment variable can also be used to override the endpoint:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint) and "auto" (auto switch to the
                default mTLS endpoint if client certificate is present, this is
                the default value). However, the ``api_endpoint`` property takes
                precedence if provided.
                (2) If GOOGLE_API_USE_CLIENT_CERTIFICATE environment variable
                is "true", then the ``client_cert_source`` property can be used
                to provide client certificate for mutual TLS transport. If
                not provided, the default SSL client certificate will be used if
                present. If GOOGLE_API_USE_CLIENT_CERTIFICATE is "false" or not
                set, no client certificate will be used.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        if isinstance(client_options, dict):
            client_options = client_options_lib.from_dict(client_options)
        if client_options is None:
            client_options = client_options_lib.ClientOptions()
        client_options = cast(client_options_lib.ClientOptions, client_options)

        api_endpoint, client_cert_source_func = self.get_mtls_endpoint_and_cert_source(
            client_options
        )

        api_key_value = getattr(client_options, "api_key", None)
        if api_key_value and credentials:
            raise ValueError(
                "client_options.api_key and credentials are mutually exclusive"
            )

        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        if isinstance(transport, CertificateManagerTransport):
            # transport is a CertificateManagerTransport instance.
            if credentials or client_options.credentials_file or api_key_value:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its credentials directly."
                )
            if client_options.scopes:
                raise ValueError(
                    "When providing a transport instance, provide its scopes "
                    "directly."
                )
            self._transport = transport
        else:
            import google.auth._default  # type: ignore

            if api_key_value and hasattr(
                google.auth._default, "get_api_key_credentials"
            ):
                credentials = google.auth._default.get_api_key_credentials(
                    api_key_value
                )

            Transport = type(self).get_transport_class(transport)
            self._transport = Transport(
                credentials=credentials,
                credentials_file=client_options.credentials_file,
                host=api_endpoint,
                scopes=client_options.scopes,
                client_cert_source_for_mtls=client_cert_source_func,
                quota_project_id=client_options.quota_project_id,
                client_info=client_info,
                always_use_jwt_access=True,
                api_audience=client_options.api_audience,
            )

    def list_certificates(
        self,
        request: Optional[
            Union[certificate_manager.ListCertificatesRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListCertificatesPager:
        r"""Lists Certificates in a given project and location.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import certificate_manager_v1

            def sample_list_certificates():
                # Create a client
                client = certificate_manager_v1.CertificateManagerClient()

                # Initialize request argument(s)
                request = certificate_manager_v1.ListCertificatesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_certificates(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.certificate_manager_v1.types.ListCertificatesRequest, dict]):
                The request object. Request for the `ListCertificates`
                method.
            parent (str):
                Required. The project and location from which the
                certificate should be listed, specified in the format
                ``projects/*/locations/*``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.certificate_manager_v1.services.certificate_manager.pagers.ListCertificatesPager:
                Response for the ListCertificates method.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a certificate_manager.ListCertificatesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, certificate_manager.ListCertificatesRequest):
            request = certificate_manager.ListCertificatesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_certificates]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListCertificatesPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_certificate(
        self,
        request: Optional[
            Union[certificate_manager.GetCertificateRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> certificate_manager.Certificate:
        r"""Gets details of a single Certificate.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import certificate_manager_v1

            def sample_get_certificate():
                # Create a client
                client = certificate_manager_v1.CertificateManagerClient()

                # Initialize request argument(s)
                request = certificate_manager_v1.GetCertificateRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_certificate(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.certificate_manager_v1.types.GetCertificateRequest, dict]):
                The request object. Request for the `GetCertificate`
                method.
            name (str):
                Required. A name of the certificate to describe. Must be
                in the format ``projects/*/locations/*/certificates/*``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.certificate_manager_v1.types.Certificate:
                Defines TLS certificate.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a certificate_manager.GetCertificateRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, certificate_manager.GetCertificateRequest):
            request = certificate_manager.GetCertificateRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_certificate]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_certificate(
        self,
        request: Optional[
            Union[certificate_manager.CreateCertificateRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        certificate: Optional[certificate_manager.Certificate] = None,
        certificate_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Creates a new Certificate in a given project and
        location.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import certificate_manager_v1

            def sample_create_certificate():
                # Create a client
                client = certificate_manager_v1.CertificateManagerClient()

                # Initialize request argument(s)
                request = certificate_manager_v1.CreateCertificateRequest(
                    parent="parent_value",
                    certificate_id="certificate_id_value",
                )

                # Make the request
                operation = client.create_certificate(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.certificate_manager_v1.types.CreateCertificateRequest, dict]):
                The request object. Request for the `CreateCertificate`
                method.
            parent (str):
                Required. The parent resource of the certificate. Must
                be in the format ``projects/*/locations/*``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            certificate (google.cloud.certificate_manager_v1.types.Certificate):
                Required. A definition of the
                certificate to create.

                This corresponds to the ``certificate`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            certificate_id (str):
                Required. A user-provided name of the
                certificate.

                This corresponds to the ``certificate_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.certificate_manager_v1.types.Certificate`
                Defines TLS certificate.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, certificate, certificate_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a certificate_manager.CreateCertificateRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, certificate_manager.CreateCertificateRequest):
            request = certificate_manager.CreateCertificateRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if certificate is not None:
                request.certificate = certificate
            if certificate_id is not None:
                request.certificate_id = certificate_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_certificate]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            certificate_manager.Certificate,
            metadata_type=certificate_manager.OperationMetadata,
        )

        # Done; return the response.
        return response

    def update_certificate(
        self,
        request: Optional[
            Union[certificate_manager.UpdateCertificateRequest, dict]
        ] = None,
        *,
        certificate: Optional[certificate_manager.Certificate] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Updates a Certificate.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import certificate_manager_v1

            def sample_update_certificate():
                # Create a client
                client = certificate_manager_v1.CertificateManagerClient()

                # Initialize request argument(s)
                request = certificate_manager_v1.UpdateCertificateRequest(
                )

                # Make the request
                operation = client.update_certificate(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.certificate_manager_v1.types.UpdateCertificateRequest, dict]):
                The request object. Request for the `UpdateCertificate`
                method.
            certificate (google.cloud.certificate_manager_v1.types.Certificate):
                Required. A definition of the
                certificate to update.

                This corresponds to the ``certificate`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Required. The update mask applies to the resource. For
                the ``FieldMask`` definition, see
                https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#fieldmask.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.certificate_manager_v1.types.Certificate`
                Defines TLS certificate.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([certificate, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a certificate_manager.UpdateCertificateRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, certificate_manager.UpdateCertificateRequest):
            request = certificate_manager.UpdateCertificateRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if certificate is not None:
                request.certificate = certificate
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_certificate]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("certificate.name", request.certificate.name),)
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            certificate_manager.Certificate,
            metadata_type=certificate_manager.OperationMetadata,
        )

        # Done; return the response.
        return response

    def delete_certificate(
        self,
        request: Optional[
            Union[certificate_manager.DeleteCertificateRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Deletes a single Certificate.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import certificate_manager_v1

            def sample_delete_certificate():
                # Create a client
                client = certificate_manager_v1.CertificateManagerClient()

                # Initialize request argument(s)
                request = certificate_manager_v1.DeleteCertificateRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_certificate(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.certificate_manager_v1.types.DeleteCertificateRequest, dict]):
                The request object. Request for the `DeleteCertificate`
                method.
            name (str):
                Required. A name of the certificate to delete. Must be
                in the format ``projects/*/locations/*/certificates/*``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.protobuf.empty_pb2.Empty` A generic empty message that you can re-use to avoid defining duplicated
                   empty messages in your APIs. A typical example is to
                   use it as the request or the response type of an API
                   method. For instance:

                      service Foo {
                         rpc Bar(google.protobuf.Empty) returns
                         (google.protobuf.Empty);

                      }

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a certificate_manager.DeleteCertificateRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, certificate_manager.DeleteCertificateRequest):
            request = certificate_manager.DeleteCertificateRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_certificate]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=certificate_manager.OperationMetadata,
        )

        # Done; return the response.
        return response

    def list_certificate_maps(
        self,
        request: Optional[
            Union[certificate_manager.ListCertificateMapsRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListCertificateMapsPager:
        r"""Lists CertificateMaps in a given project and
        location.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import certificate_manager_v1

            def sample_list_certificate_maps():
                # Create a client
                client = certificate_manager_v1.CertificateManagerClient()

                # Initialize request argument(s)
                request = certificate_manager_v1.ListCertificateMapsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_certificate_maps(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.certificate_manager_v1.types.ListCertificateMapsRequest, dict]):
                The request object. Request for the
                `ListCertificateMaps` method.
            parent (str):
                Required. The project and location from which the
                certificate maps should be listed, specified in the
                format ``projects/*/locations/*``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.certificate_manager_v1.services.certificate_manager.pagers.ListCertificateMapsPager:
                Response for the ListCertificateMaps method.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a certificate_manager.ListCertificateMapsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, certificate_manager.ListCertificateMapsRequest):
            request = certificate_manager.ListCertificateMapsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_certificate_maps]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListCertificateMapsPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_certificate_map(
        self,
        request: Optional[
            Union[certificate_manager.GetCertificateMapRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> certificate_manager.CertificateMap:
        r"""Gets details of a single CertificateMap.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import certificate_manager_v1

            def sample_get_certificate_map():
                # Create a client
                client = certificate_manager_v1.CertificateManagerClient()

                # Initialize request argument(s)
                request = certificate_manager_v1.GetCertificateMapRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_certificate_map(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.certificate_manager_v1.types.GetCertificateMapRequest, dict]):
                The request object. Request for the `GetCertificateMap`
                method.
            name (str):
                Required. A name of the certificate map to describe.
                Must be in the format
                ``projects/*/locations/*/certificateMaps/*``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.certificate_manager_v1.types.CertificateMap:
                Defines a collection of certificate
                configurations.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a certificate_manager.GetCertificateMapRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, certificate_manager.GetCertificateMapRequest):
            request = certificate_manager.GetCertificateMapRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_certificate_map]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_certificate_map(
        self,
        request: Optional[
            Union[certificate_manager.CreateCertificateMapRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        certificate_map: Optional[certificate_manager.CertificateMap] = None,
        certificate_map_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Creates a new CertificateMap in a given project and
        location.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import certificate_manager_v1

            def sample_create_certificate_map():
                # Create a client
                client = certificate_manager_v1.CertificateManagerClient()

                # Initialize request argument(s)
                request = certificate_manager_v1.CreateCertificateMapRequest(
                    parent="parent_value",
                    certificate_map_id="certificate_map_id_value",
                )

                # Make the request
                operation = client.create_certificate_map(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.certificate_manager_v1.types.CreateCertificateMapRequest, dict]):
                The request object. Request for the
                `CreateCertificateMap` method.
            parent (str):
                Required. The parent resource of the certificate map.
                Must be in the format ``projects/*/locations/*``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            certificate_map (google.cloud.certificate_manager_v1.types.CertificateMap):
                Required. A definition of the
                certificate map to create.

                This corresponds to the ``certificate_map`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            certificate_map_id (str):
                Required. A user-provided name of the
                certificate map.

                This corresponds to the ``certificate_map_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.certificate_manager_v1.types.CertificateMap`
                Defines a collection of certificate configurations.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, certificate_map, certificate_map_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a certificate_manager.CreateCertificateMapRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, certificate_manager.CreateCertificateMapRequest):
            request = certificate_manager.CreateCertificateMapRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if certificate_map is not None:
                request.certificate_map = certificate_map
            if certificate_map_id is not None:
                request.certificate_map_id = certificate_map_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_certificate_map]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            certificate_manager.CertificateMap,
            metadata_type=certificate_manager.OperationMetadata,
        )

        # Done; return the response.
        return response

    def update_certificate_map(
        self,
        request: Optional[
            Union[certificate_manager.UpdateCertificateMapRequest, dict]
        ] = None,
        *,
        certificate_map: Optional[certificate_manager.CertificateMap] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Updates a CertificateMap.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import certificate_manager_v1

            def sample_update_certificate_map():
                # Create a client
                client = certificate_manager_v1.CertificateManagerClient()

                # Initialize request argument(s)
                request = certificate_manager_v1.UpdateCertificateMapRequest(
                )

                # Make the request
                operation = client.update_certificate_map(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.certificate_manager_v1.types.UpdateCertificateMapRequest, dict]):
                The request object. Request for the
                `UpdateCertificateMap` method.
            certificate_map (google.cloud.certificate_manager_v1.types.CertificateMap):
                Required. A definition of the
                certificate map to update.

                This corresponds to the ``certificate_map`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Required. The update mask applies to the resource. For
                the ``FieldMask`` definition, see
                https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#fieldmask.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.certificate_manager_v1.types.CertificateMap`
                Defines a collection of certificate configurations.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([certificate_map, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a certificate_manager.UpdateCertificateMapRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, certificate_manager.UpdateCertificateMapRequest):
            request = certificate_manager.UpdateCertificateMapRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if certificate_map is not None:
                request.certificate_map = certificate_map
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_certificate_map]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("certificate_map.name", request.certificate_map.name),)
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            certificate_manager.CertificateMap,
            metadata_type=certificate_manager.OperationMetadata,
        )

        # Done; return the response.
        return response

    def delete_certificate_map(
        self,
        request: Optional[
            Union[certificate_manager.DeleteCertificateMapRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Deletes a single CertificateMap. A Certificate Map
        can't be deleted if it contains Certificate Map Entries.
        Remove all the entries from the map before calling this
        method.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import certificate_manager_v1

            def sample_delete_certificate_map():
                # Create a client
                client = certificate_manager_v1.CertificateManagerClient()

                # Initialize request argument(s)
                request = certificate_manager_v1.DeleteCertificateMapRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_certificate_map(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.certificate_manager_v1.types.DeleteCertificateMapRequest, dict]):
                The request object. Request for the
                `DeleteCertificateMap` method.
            name (str):
                Required. A name of the certificate map to delete. Must
                be in the format
                ``projects/*/locations/*/certificateMaps/*``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.protobuf.empty_pb2.Empty` A generic empty message that you can re-use to avoid defining duplicated
                   empty messages in your APIs. A typical example is to
                   use it as the request or the response type of an API
                   method. For instance:

                      service Foo {
                         rpc Bar(google.protobuf.Empty) returns
                         (google.protobuf.Empty);

                      }

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a certificate_manager.DeleteCertificateMapRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, certificate_manager.DeleteCertificateMapRequest):
            request = certificate_manager.DeleteCertificateMapRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_certificate_map]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=certificate_manager.OperationMetadata,
        )

        # Done; return the response.
        return response

    def list_certificate_map_entries(
        self,
        request: Optional[
            Union[certificate_manager.ListCertificateMapEntriesRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListCertificateMapEntriesPager:
        r"""Lists CertificateMapEntries in a given project and
        location.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import certificate_manager_v1

            def sample_list_certificate_map_entries():
                # Create a client
                client = certificate_manager_v1.CertificateManagerClient()

                # Initialize request argument(s)
                request = certificate_manager_v1.ListCertificateMapEntriesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_certificate_map_entries(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.certificate_manager_v1.types.ListCertificateMapEntriesRequest, dict]):
                The request object. Request for the
                `ListCertificateMapEntries` method.
            parent (str):
                Required. The project, location and certificate map from
                which the certificate map entries should be listed,
                specified in the format
                ``projects/*/locations/*/certificateMaps/*``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.certificate_manager_v1.services.certificate_manager.pagers.ListCertificateMapEntriesPager:
                Response for the ListCertificateMapEntries method.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a certificate_manager.ListCertificateMapEntriesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, certificate_manager.ListCertificateMapEntriesRequest
        ):
            request = certificate_manager.ListCertificateMapEntriesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.list_certificate_map_entries
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListCertificateMapEntriesPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_certificate_map_entry(
        self,
        request: Optional[
            Union[certificate_manager.GetCertificateMapEntryRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> certificate_manager.CertificateMapEntry:
        r"""Gets details of a single CertificateMapEntry.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import certificate_manager_v1

            def sample_get_certificate_map_entry():
                # Create a client
                client = certificate_manager_v1.CertificateManagerClient()

                # Initialize request argument(s)
                request = certificate_manager_v1.GetCertificateMapEntryRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_certificate_map_entry(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.certificate_manager_v1.types.GetCertificateMapEntryRequest, dict]):
                The request object. Request for the
                `GetCertificateMapEntry` method.
            name (str):
                Required. A name of the certificate map entry to
                describe. Must be in the format
                ``projects/*/locations/*/certificateMaps/*/certificateMapEntries/*``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.certificate_manager_v1.types.CertificateMapEntry:
                Defines a certificate map entry.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a certificate_manager.GetCertificateMapEntryRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, certificate_manager.GetCertificateMapEntryRequest):
            request = certificate_manager.GetCertificateMapEntryRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.get_certificate_map_entry
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_certificate_map_entry(
        self,
        request: Optional[
            Union[certificate_manager.CreateCertificateMapEntryRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        certificate_map_entry: Optional[certificate_manager.CertificateMapEntry] = None,
        certificate_map_entry_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Creates a new CertificateMapEntry in a given project
        and location.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import certificate_manager_v1

            def sample_create_certificate_map_entry():
                # Create a client
                client = certificate_manager_v1.CertificateManagerClient()

                # Initialize request argument(s)
                certificate_map_entry = certificate_manager_v1.CertificateMapEntry()
                certificate_map_entry.hostname = "hostname_value"

                request = certificate_manager_v1.CreateCertificateMapEntryRequest(
                    parent="parent_value",
                    certificate_map_entry_id="certificate_map_entry_id_value",
                    certificate_map_entry=certificate_map_entry,
                )

                # Make the request
                operation = client.create_certificate_map_entry(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.certificate_manager_v1.types.CreateCertificateMapEntryRequest, dict]):
                The request object. Request for the
                `CreateCertificateMapEntry` method.
            parent (str):
                Required. The parent resource of the certificate map
                entry. Must be in the format
                ``projects/*/locations/*/certificateMaps/*``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            certificate_map_entry (google.cloud.certificate_manager_v1.types.CertificateMapEntry):
                Required. A definition of the
                certificate map entry to create.

                This corresponds to the ``certificate_map_entry`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            certificate_map_entry_id (str):
                Required. A user-provided name of the
                certificate map entry.

                This corresponds to the ``certificate_map_entry_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.certificate_manager_v1.types.CertificateMapEntry`
                Defines a certificate map entry.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [parent, certificate_map_entry, certificate_map_entry_id]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a certificate_manager.CreateCertificateMapEntryRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, certificate_manager.CreateCertificateMapEntryRequest
        ):
            request = certificate_manager.CreateCertificateMapEntryRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if certificate_map_entry is not None:
                request.certificate_map_entry = certificate_map_entry
            if certificate_map_entry_id is not None:
                request.certificate_map_entry_id = certificate_map_entry_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.create_certificate_map_entry
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            certificate_manager.CertificateMapEntry,
            metadata_type=certificate_manager.OperationMetadata,
        )

        # Done; return the response.
        return response

    def update_certificate_map_entry(
        self,
        request: Optional[
            Union[certificate_manager.UpdateCertificateMapEntryRequest, dict]
        ] = None,
        *,
        certificate_map_entry: Optional[certificate_manager.CertificateMapEntry] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Updates a CertificateMapEntry.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import certificate_manager_v1

            def sample_update_certificate_map_entry():
                # Create a client
                client = certificate_manager_v1.CertificateManagerClient()

                # Initialize request argument(s)
                certificate_map_entry = certificate_manager_v1.CertificateMapEntry()
                certificate_map_entry.hostname = "hostname_value"

                request = certificate_manager_v1.UpdateCertificateMapEntryRequest(
                    certificate_map_entry=certificate_map_entry,
                )

                # Make the request
                operation = client.update_certificate_map_entry(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.certificate_manager_v1.types.UpdateCertificateMapEntryRequest, dict]):
                The request object. Request for the
                `UpdateCertificateMapEntry` method.
            certificate_map_entry (google.cloud.certificate_manager_v1.types.CertificateMapEntry):
                Required. A definition of the
                certificate map entry to create map
                entry.

                This corresponds to the ``certificate_map_entry`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Required. The update mask applies to the resource. For
                the ``FieldMask`` definition, see
                https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#fieldmask.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.certificate_manager_v1.types.CertificateMapEntry`
                Defines a certificate map entry.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([certificate_map_entry, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a certificate_manager.UpdateCertificateMapEntryRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, certificate_manager.UpdateCertificateMapEntryRequest
        ):
            request = certificate_manager.UpdateCertificateMapEntryRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if certificate_map_entry is not None:
                request.certificate_map_entry = certificate_map_entry
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.update_certificate_map_entry
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("certificate_map_entry.name", request.certificate_map_entry.name),)
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            certificate_manager.CertificateMapEntry,
            metadata_type=certificate_manager.OperationMetadata,
        )

        # Done; return the response.
        return response

    def delete_certificate_map_entry(
        self,
        request: Optional[
            Union[certificate_manager.DeleteCertificateMapEntryRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Deletes a single CertificateMapEntry.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import certificate_manager_v1

            def sample_delete_certificate_map_entry():
                # Create a client
                client = certificate_manager_v1.CertificateManagerClient()

                # Initialize request argument(s)
                request = certificate_manager_v1.DeleteCertificateMapEntryRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_certificate_map_entry(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.certificate_manager_v1.types.DeleteCertificateMapEntryRequest, dict]):
                The request object. Request for the
                `DeleteCertificateMapEntry` method.
            name (str):
                Required. A name of the certificate map entry to delete.
                Must be in the format
                ``projects/*/locations/*/certificateMaps/*/certificateMapEntries/*``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.protobuf.empty_pb2.Empty` A generic empty message that you can re-use to avoid defining duplicated
                   empty messages in your APIs. A typical example is to
                   use it as the request or the response type of an API
                   method. For instance:

                      service Foo {
                         rpc Bar(google.protobuf.Empty) returns
                         (google.protobuf.Empty);

                      }

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a certificate_manager.DeleteCertificateMapEntryRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, certificate_manager.DeleteCertificateMapEntryRequest
        ):
            request = certificate_manager.DeleteCertificateMapEntryRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.delete_certificate_map_entry
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=certificate_manager.OperationMetadata,
        )

        # Done; return the response.
        return response

    def list_dns_authorizations(
        self,
        request: Optional[
            Union[certificate_manager.ListDnsAuthorizationsRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListDnsAuthorizationsPager:
        r"""Lists DnsAuthorizations in a given project and
        location.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import certificate_manager_v1

            def sample_list_dns_authorizations():
                # Create a client
                client = certificate_manager_v1.CertificateManagerClient()

                # Initialize request argument(s)
                request = certificate_manager_v1.ListDnsAuthorizationsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_dns_authorizations(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.certificate_manager_v1.types.ListDnsAuthorizationsRequest, dict]):
                The request object. Request for the
                `ListDnsAuthorizations` method.
            parent (str):
                Required. The project and location from which the dns
                authorizations should be listed, specified in the format
                ``projects/*/locations/*``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.certificate_manager_v1.services.certificate_manager.pagers.ListDnsAuthorizationsPager:
                Response for the ListDnsAuthorizations method.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a certificate_manager.ListDnsAuthorizationsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, certificate_manager.ListDnsAuthorizationsRequest):
            request = certificate_manager.ListDnsAuthorizationsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_dns_authorizations]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListDnsAuthorizationsPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_dns_authorization(
        self,
        request: Optional[
            Union[certificate_manager.GetDnsAuthorizationRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> certificate_manager.DnsAuthorization:
        r"""Gets details of a single DnsAuthorization.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import certificate_manager_v1

            def sample_get_dns_authorization():
                # Create a client
                client = certificate_manager_v1.CertificateManagerClient()

                # Initialize request argument(s)
                request = certificate_manager_v1.GetDnsAuthorizationRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_dns_authorization(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.certificate_manager_v1.types.GetDnsAuthorizationRequest, dict]):
                The request object. Request for the
                `GetDnsAuthorization` method.
            name (str):
                Required. A name of the dns authorization to describe.
                Must be in the format
                ``projects/*/locations/*/dnsAuthorizations/*``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.certificate_manager_v1.types.DnsAuthorization:
                A DnsAuthorization resource describes
                a way to perform domain authorization
                for certificate issuance.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a certificate_manager.GetDnsAuthorizationRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, certificate_manager.GetDnsAuthorizationRequest):
            request = certificate_manager.GetDnsAuthorizationRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_dns_authorization]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_dns_authorization(
        self,
        request: Optional[
            Union[certificate_manager.CreateDnsAuthorizationRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        dns_authorization: Optional[certificate_manager.DnsAuthorization] = None,
        dns_authorization_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Creates a new DnsAuthorization in a given project and
        location.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import certificate_manager_v1

            def sample_create_dns_authorization():
                # Create a client
                client = certificate_manager_v1.CertificateManagerClient()

                # Initialize request argument(s)
                dns_authorization = certificate_manager_v1.DnsAuthorization()
                dns_authorization.domain = "domain_value"

                request = certificate_manager_v1.CreateDnsAuthorizationRequest(
                    parent="parent_value",
                    dns_authorization_id="dns_authorization_id_value",
                    dns_authorization=dns_authorization,
                )

                # Make the request
                operation = client.create_dns_authorization(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.certificate_manager_v1.types.CreateDnsAuthorizationRequest, dict]):
                The request object. Request for the
                `CreateDnsAuthorization` method.
            parent (str):
                Required. The parent resource of the dns authorization.
                Must be in the format ``projects/*/locations/*``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            dns_authorization (google.cloud.certificate_manager_v1.types.DnsAuthorization):
                Required. A definition of the dns
                authorization to create.

                This corresponds to the ``dns_authorization`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            dns_authorization_id (str):
                Required. A user-provided name of the
                dns authorization.

                This corresponds to the ``dns_authorization_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.certificate_manager_v1.types.DnsAuthorization` A DnsAuthorization resource describes a way to perform domain authorization
                   for certificate issuance.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, dns_authorization, dns_authorization_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a certificate_manager.CreateDnsAuthorizationRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, certificate_manager.CreateDnsAuthorizationRequest):
            request = certificate_manager.CreateDnsAuthorizationRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if dns_authorization is not None:
                request.dns_authorization = dns_authorization
            if dns_authorization_id is not None:
                request.dns_authorization_id = dns_authorization_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_dns_authorization]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            certificate_manager.DnsAuthorization,
            metadata_type=certificate_manager.OperationMetadata,
        )

        # Done; return the response.
        return response

    def update_dns_authorization(
        self,
        request: Optional[
            Union[certificate_manager.UpdateDnsAuthorizationRequest, dict]
        ] = None,
        *,
        dns_authorization: Optional[certificate_manager.DnsAuthorization] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Updates a DnsAuthorization.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import certificate_manager_v1

            def sample_update_dns_authorization():
                # Create a client
                client = certificate_manager_v1.CertificateManagerClient()

                # Initialize request argument(s)
                dns_authorization = certificate_manager_v1.DnsAuthorization()
                dns_authorization.domain = "domain_value"

                request = certificate_manager_v1.UpdateDnsAuthorizationRequest(
                    dns_authorization=dns_authorization,
                )

                # Make the request
                operation = client.update_dns_authorization(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.certificate_manager_v1.types.UpdateDnsAuthorizationRequest, dict]):
                The request object. Request for the
                `UpdateDnsAuthorization` method.
            dns_authorization (google.cloud.certificate_manager_v1.types.DnsAuthorization):
                Required. A definition of the dns
                authorization to update.

                This corresponds to the ``dns_authorization`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Required. The update mask applies to the resource. For
                the ``FieldMask`` definition, see
                https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#fieldmask.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.certificate_manager_v1.types.DnsAuthorization` A DnsAuthorization resource describes a way to perform domain authorization
                   for certificate issuance.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([dns_authorization, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a certificate_manager.UpdateDnsAuthorizationRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, certificate_manager.UpdateDnsAuthorizationRequest):
            request = certificate_manager.UpdateDnsAuthorizationRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if dns_authorization is not None:
                request.dns_authorization = dns_authorization
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_dns_authorization]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("dns_authorization.name", request.dns_authorization.name),)
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            certificate_manager.DnsAuthorization,
            metadata_type=certificate_manager.OperationMetadata,
        )

        # Done; return the response.
        return response

    def delete_dns_authorization(
        self,
        request: Optional[
            Union[certificate_manager.DeleteDnsAuthorizationRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Deletes a single DnsAuthorization.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import certificate_manager_v1

            def sample_delete_dns_authorization():
                # Create a client
                client = certificate_manager_v1.CertificateManagerClient()

                # Initialize request argument(s)
                request = certificate_manager_v1.DeleteDnsAuthorizationRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_dns_authorization(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.certificate_manager_v1.types.DeleteDnsAuthorizationRequest, dict]):
                The request object. Request for the
                `DeleteDnsAuthorization` method.
            name (str):
                Required. A name of the dns authorization to delete.
                Must be in the format
                ``projects/*/locations/*/dnsAuthorizations/*``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.protobuf.empty_pb2.Empty` A generic empty message that you can re-use to avoid defining duplicated
                   empty messages in your APIs. A typical example is to
                   use it as the request or the response type of an API
                   method. For instance:

                      service Foo {
                         rpc Bar(google.protobuf.Empty) returns
                         (google.protobuf.Empty);

                      }

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a certificate_manager.DeleteDnsAuthorizationRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, certificate_manager.DeleteDnsAuthorizationRequest):
            request = certificate_manager.DeleteDnsAuthorizationRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_dns_authorization]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=certificate_manager.OperationMetadata,
        )

        # Done; return the response.
        return response

    def list_certificate_issuance_configs(
        self,
        request: Optional[
            Union[
                certificate_issuance_config.ListCertificateIssuanceConfigsRequest, dict
            ]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListCertificateIssuanceConfigsPager:
        r"""Lists CertificateIssuanceConfigs in a given project
        and location.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import certificate_manager_v1

            def sample_list_certificate_issuance_configs():
                # Create a client
                client = certificate_manager_v1.CertificateManagerClient()

                # Initialize request argument(s)
                request = certificate_manager_v1.ListCertificateIssuanceConfigsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_certificate_issuance_configs(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.certificate_manager_v1.types.ListCertificateIssuanceConfigsRequest, dict]):
                The request object. Request for the
                `ListCertificateIssuanceConfigs` method.
            parent (str):
                Required. The project and location from which the
                certificate should be listed, specified in the format
                ``projects/*/locations/*``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.certificate_manager_v1.services.certificate_manager.pagers.ListCertificateIssuanceConfigsPager:
                Response for the ListCertificateIssuanceConfigs method.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a certificate_issuance_config.ListCertificateIssuanceConfigsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, certificate_issuance_config.ListCertificateIssuanceConfigsRequest
        ):
            request = certificate_issuance_config.ListCertificateIssuanceConfigsRequest(
                request
            )
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.list_certificate_issuance_configs
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListCertificateIssuanceConfigsPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_certificate_issuance_config(
        self,
        request: Optional[
            Union[certificate_issuance_config.GetCertificateIssuanceConfigRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> certificate_issuance_config.CertificateIssuanceConfig:
        r"""Gets details of a single CertificateIssuanceConfig.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import certificate_manager_v1

            def sample_get_certificate_issuance_config():
                # Create a client
                client = certificate_manager_v1.CertificateManagerClient()

                # Initialize request argument(s)
                request = certificate_manager_v1.GetCertificateIssuanceConfigRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_certificate_issuance_config(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.certificate_manager_v1.types.GetCertificateIssuanceConfigRequest, dict]):
                The request object. Request for the
                `GetCertificateIssuanceConfig` method.
            name (str):
                Required. A name of the certificate issuance config to
                describe. Must be in the format
                ``projects/*/locations/*/certificateIssuanceConfigs/*``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.certificate_manager_v1.types.CertificateIssuanceConfig:
                CertificateIssuanceConfig specifies
                how to issue and manage a certificate.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a certificate_issuance_config.GetCertificateIssuanceConfigRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, certificate_issuance_config.GetCertificateIssuanceConfigRequest
        ):
            request = certificate_issuance_config.GetCertificateIssuanceConfigRequest(
                request
            )
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.get_certificate_issuance_config
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_certificate_issuance_config(
        self,
        request: Optional[
            Union[
                gcc_certificate_issuance_config.CreateCertificateIssuanceConfigRequest,
                dict,
            ]
        ] = None,
        *,
        parent: Optional[str] = None,
        certificate_issuance_config: Optional[
            gcc_certificate_issuance_config.CertificateIssuanceConfig
        ] = None,
        certificate_issuance_config_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Creates a new CertificateIssuanceConfig in a given
        project and location.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import certificate_manager_v1

            def sample_create_certificate_issuance_config():
                # Create a client
                client = certificate_manager_v1.CertificateManagerClient()

                # Initialize request argument(s)
                certificate_issuance_config = certificate_manager_v1.CertificateIssuanceConfig()
                certificate_issuance_config.certificate_authority_config.certificate_authority_service_config.ca_pool = "ca_pool_value"
                certificate_issuance_config.rotation_window_percentage = 2788
                certificate_issuance_config.key_algorithm = "ECDSA_P256"

                request = certificate_manager_v1.CreateCertificateIssuanceConfigRequest(
                    parent="parent_value",
                    certificate_issuance_config_id="certificate_issuance_config_id_value",
                    certificate_issuance_config=certificate_issuance_config,
                )

                # Make the request
                operation = client.create_certificate_issuance_config(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.certificate_manager_v1.types.CreateCertificateIssuanceConfigRequest, dict]):
                The request object. Request for the
                `CreateCertificateIssuanceConfig` method.
            parent (str):
                Required. The parent resource of the certificate
                issuance config. Must be in the format
                ``projects/*/locations/*``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            certificate_issuance_config (google.cloud.certificate_manager_v1.types.CertificateIssuanceConfig):
                Required. A definition of the
                certificate issuance config to create.

                This corresponds to the ``certificate_issuance_config`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            certificate_issuance_config_id (str):
                Required. A user-provided name of the
                certificate config.

                This corresponds to the ``certificate_issuance_config_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.certificate_manager_v1.types.CertificateIssuanceConfig`
                CertificateIssuanceConfig specifies how to issue and
                manage a certificate.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [parent, certificate_issuance_config, certificate_issuance_config_id]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a gcc_certificate_issuance_config.CreateCertificateIssuanceConfigRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request,
            gcc_certificate_issuance_config.CreateCertificateIssuanceConfigRequest,
        ):
            request = (
                gcc_certificate_issuance_config.CreateCertificateIssuanceConfigRequest(
                    request
                )
            )
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if certificate_issuance_config is not None:
                request.certificate_issuance_config = certificate_issuance_config
            if certificate_issuance_config_id is not None:
                request.certificate_issuance_config_id = certificate_issuance_config_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.create_certificate_issuance_config
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            gcc_certificate_issuance_config.CertificateIssuanceConfig,
            metadata_type=certificate_manager.OperationMetadata,
        )

        # Done; return the response.
        return response

    def delete_certificate_issuance_config(
        self,
        request: Optional[
            Union[
                certificate_issuance_config.DeleteCertificateIssuanceConfigRequest, dict
            ]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Deletes a single CertificateIssuanceConfig.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import certificate_manager_v1

            def sample_delete_certificate_issuance_config():
                # Create a client
                client = certificate_manager_v1.CertificateManagerClient()

                # Initialize request argument(s)
                request = certificate_manager_v1.DeleteCertificateIssuanceConfigRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_certificate_issuance_config(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.certificate_manager_v1.types.DeleteCertificateIssuanceConfigRequest, dict]):
                The request object. Request for the
                `DeleteCertificateIssuanceConfig` method.
            name (str):
                Required. A name of the certificate issuance config to
                delete. Must be in the format
                ``projects/*/locations/*/certificateIssuanceConfigs/*``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.protobuf.empty_pb2.Empty` A generic empty message that you can re-use to avoid defining duplicated
                   empty messages in your APIs. A typical example is to
                   use it as the request or the response type of an API
                   method. For instance:

                      service Foo {
                         rpc Bar(google.protobuf.Empty) returns
                         (google.protobuf.Empty);

                      }

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a certificate_issuance_config.DeleteCertificateIssuanceConfigRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, certificate_issuance_config.DeleteCertificateIssuanceConfigRequest
        ):
            request = (
                certificate_issuance_config.DeleteCertificateIssuanceConfigRequest(
                    request
                )
            )
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.delete_certificate_issuance_config
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=certificate_manager.OperationMetadata,
        )

        # Done; return the response.
        return response

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        """Releases underlying transport's resources.

        .. warning::
            ONLY use as a context manager if the transport is NOT shared
            with other clients! Exiting the with block will CLOSE the transport
            and may cause errors in other clients!
        """
        self.transport.close()

    def list_operations(
        self,
        request: Optional[operations_pb2.ListOperationsRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operations_pb2.ListOperationsResponse:
        r"""Lists operations that match the specified filter in the request.

        Args:
            request (:class:`~.operations_pb2.ListOperationsRequest`):
                The request object. Request message for
                `ListOperations` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                    if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            ~.operations_pb2.ListOperationsResponse:
                Response message for ``ListOperations`` method.
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = operations_pb2.ListOperationsRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.list_operations,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_operation(
        self,
        request: Optional[operations_pb2.GetOperationRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operations_pb2.Operation:
        r"""Gets the latest state of a long-running operation.

        Args:
            request (:class:`~.operations_pb2.GetOperationRequest`):
                The request object. Request message for
                `GetOperation` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                    if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            ~.operations_pb2.Operation:
                An ``Operation`` object.
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = operations_pb2.GetOperationRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.get_operation,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_operation(
        self,
        request: Optional[operations_pb2.DeleteOperationRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a long-running operation.

        This method indicates that the client is no longer interested
        in the operation result. It does not cancel the operation.
        If the server doesn't support this method, it returns
        `google.rpc.Code.UNIMPLEMENTED`.

        Args:
            request (:class:`~.operations_pb2.DeleteOperationRequest`):
                The request object. Request message for
                `DeleteOperation` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                    if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            None
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = operations_pb2.DeleteOperationRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.delete_operation,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def cancel_operation(
        self,
        request: Optional[operations_pb2.CancelOperationRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Starts asynchronous cancellation on a long-running operation.

        The server makes a best effort to cancel the operation, but success
        is not guaranteed.  If the server doesn't support this method, it returns
        `google.rpc.Code.UNIMPLEMENTED`.

        Args:
            request (:class:`~.operations_pb2.CancelOperationRequest`):
                The request object. Request message for
                `CancelOperation` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                    if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            None
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = operations_pb2.CancelOperationRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.cancel_operation,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def get_location(
        self,
        request: Optional[locations_pb2.GetLocationRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> locations_pb2.Location:
        r"""Gets information about a location.

        Args:
            request (:class:`~.location_pb2.GetLocationRequest`):
                The request object. Request message for
                `GetLocation` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                 if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            ~.location_pb2.Location:
                Location object.
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = locations_pb2.GetLocationRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.get_location,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_locations(
        self,
        request: Optional[locations_pb2.ListLocationsRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> locations_pb2.ListLocationsResponse:
        r"""Lists information about the supported locations for this service.

        Args:
            request (:class:`~.location_pb2.ListLocationsRequest`):
                The request object. Request message for
                `ListLocations` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                 if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            ~.location_pb2.ListLocationsResponse:
                Response message for ``ListLocations`` method.
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = locations_pb2.ListLocationsRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.list_locations,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


__all__ = ("CertificateManagerClient",)
