using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
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
            _dbService = dbService;
        }
        
        // GET api/savedAcordaos
        [HttpGet]
        public async Task<ActionResult<IEnumerable<SavedAcordaoDto>>> Get()
        {
           var result = await _dbService.GetSavedAcordaos();
           return result.Select(x => SavedAcordaoDto.FromEntity(x)).ToList();
        }

        // GET api/savedAcordaos/5
        [HttpGet("{id}")]
        public async Task<ActionResult<SavedAcordaoDto>> Get(int id)
        {
            var sa = await _dbService.GetSavedAcordao(id);
            return SavedAcordaoDto.FromEntity(sa);
        }


    }
}
