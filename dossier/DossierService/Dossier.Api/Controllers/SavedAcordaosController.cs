using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Dossier.Core.Services;
using Dossier.Api.Models;
using Dossier.Core.Interfaces;

namespace Dossier.Api.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class SavedAcordaosController : ControllerBase
    {
        private readonly IDbService _dbService;
        
        public SavedAcordaosController(IDbService dbService) {
            _dbService = _dbService;
        }
        
        // GET api/savedAcordaos
        [HttpGet]
        public ActionResult<IEnumerable<SavedAcordao>> Get()
        {
           var result = _dbService.GetSavedAcordaos().ToList();

           return result.Select(x => new SavedAcordao() {
               AcordaoId = x.OriginalAcordaoId,
               Comments = x.Comments
           }).ToList();
        }

        // GET api/savedAcordaos/5
        [HttpGet("{id}")]
        public ActionResult<string> Get(int id)
        {
            return "savedAcordao";
        }


    }
}
