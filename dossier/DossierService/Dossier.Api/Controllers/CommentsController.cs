using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Dossier.Api.Models;
using Dossier.Core.Interfaces;
using Dossier.Core.Entities;

namespace Dossier.Api.Controllers
{
    [ApiVersion("1.0")]
    [Route("api/v{version:apiVersion}/[controller]")]
    [ApiController]
    public class CommentsController : ControllerBase
    {
        private readonly IDbService _dbService;
        
        public CommentsController(IDbService dbService) {
            _dbService = dbService;
        }
        
        // GET api/comments/5
        [HttpGet("{id}")]
        public async Task<ActionResult<CommentDto>> Get(int id)
        {
            var sa = await _dbService.GetComment(id);
            return CommentDto.FromEntity(sa);
        }
    }
}
