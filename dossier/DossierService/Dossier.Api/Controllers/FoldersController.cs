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
    public class FoldersController : ControllerBase
    {
        private readonly IDbService _dbService;
        
        public FoldersController(IDbService dbService) {
            _dbService = dbService;
        }
        
        // TODO make other controller actions async
        // GET api/folders
        [HttpGet]
        public async Task<ActionResult<IEnumerable<FolderDto>>> Get()
        {
           var result = await _dbService.GetFolders();

           return result.Select(x => FolderDto.FromEntity(x)).ToList();
        }

        // GET api/folders/5
        [HttpGet("{id}")]
        public async Task<ActionResult<FolderDto>> Get(int id)
        {
            var result = await _dbService.GetFolder(id);
            return FolderDto.FromEntity(result);
        }


    }
}
