using System;
using Microsoft.AspNetCore.Mvc;

namespace Dossier.Api.Controllers
{
    [ApiController]
    public abstract class DossierBaseController : ControllerBase
    {
   //     protected string ApiVersion => HttpContext.GetRequestedApiVersion().ToString();
    }
}
