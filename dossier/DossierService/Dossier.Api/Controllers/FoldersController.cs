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
    public class FoldersController : ControllerBase
    {
        private IFolderService _folderService;
        private readonly IDbService _dbService;
        
        public FoldersController(IFolderService folderService, IDbService dbService) {
            _folderService = folderService;
            _dbService = _dbService;
        }
        
        // GET api/folders
        [HttpGet]
        public ActionResult<IEnumerable<Folder>> Get()
        {
           var result = _dbService.GetFolders().ToList();

           return result.Select(x => new Folder() {
               Name = x.Name,
               Acordaos = x.SavedAcordaos.Select(a => a.Id)
           }).ToList();
        }

        // GET api/folders/5
        [HttpGet("{id}")]
        public ActionResult<string> Get(int id)
        {
            return "folder";
        }


    }
}
