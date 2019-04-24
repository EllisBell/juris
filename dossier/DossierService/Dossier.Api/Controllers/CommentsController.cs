using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Dossier.Api.Models;
using Dossier.Core.Interfaces;
using Dossier.Core.Entities;
using Dossier.Core.Exceptions;

namespace Dossier.Api.Controllers
{
    [ApiVersion("1.0")]
    [Route("api/v{version:apiVersion}/[controller]")]
    [ApiController]
    public class CommentsController : DossierBaseController
    {
        private readonly IDbService _dbService;
        
        public CommentsController(IDbService dbService) 
        {
            _dbService = dbService;
        }
        
        // GET api/comments/5
        [HttpGet("{id}")]
        public async Task<ActionResult<CommentDto>> Get(int id)
        {
            var comment = await _dbService.GetComment(id);
            
            if(comment is null)
                return NotFound();

            return CommentDto.FromEntity(comment);
        }

        // PATCH api/comments/5
        [HttpPatch("{id}")]
        public async Task<ActionResult<CommentDto>> UpdateComment(int id, CommentUpdateDto commentDto) 
        {
            try 
            {
                await _dbService.UpdateCommentText(id, commentDto.Text);
                var commentEntity = await _dbService.GetComment(id);
                return CommentDto.FromEntity(commentEntity);
            }
            catch(NotFoundException) 
            {
                return NotFound();
            }
        }

        // DELETE api/comments/5
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteComment(int id) {
            try 
            {
                await _dbService.DeleteComment(id);
                return NoContent();
            }
            catch(NotFoundException) {
                return NotFound();
            }
        }
    }
}
