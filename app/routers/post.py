from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", response_model=list[schemas.ReturnPost])
async def get_post(db: Session = Depends(get_db), get_current_user: models.User = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: str = ""):
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).offset(skip).limit(limit).all()
    result = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True
    ).group_by(models.Post.id).filter(models.Post.title.contains(search)).offset(skip).limit(limit).all()

    posts_with_votes = []
    for post, votes in result:
        posts_with_votes.append(schemas.ReturnPost(
            id=post.id,
            user_id=post.user_id,
            title=post.title,
            content=post.content,
            published=post.published,
            created_at=post.created_at,
            owner=schemas.UserOut(
                id=post.owner.id,
                email=post.owner.email,
                created_at=post.owner.created_at
            ),
            votes=votes
        ))
    return posts_with_votes

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ReturnPost)
async def create_posts(post: schemas.Post, db: Session = Depends(get_db), get_current_user: models.User = Depends(oauth2.get_current_user)):
    print(get_current_user)
    user_id = get_current_user.id
    new_post = models.Post(title=post.title, content=post.content, published=post.published, user_id = user_id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=schemas.ReturnPost)
# @router.get("/{id}")
async def get_post(id: int, db: Session = Depends(get_db), get_current_user: models.User = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    # post = db.query(models.Post).filter(models.Post.id == id).options(joinedload(models.Post.owner)).first()
    
    if post:
        return schemas.ReturnPost(
            id=post.id,
            user_id=post.user_id,
            title=post.title,
            content=post.content,
            published=post.published,
            created_at=post.created_at,
            owner=schemas.UserOut(
                id=post.owner.id,
                email=post.owner.email,
                created_at=post.owner.created_at
            ),
            votes=db.query(models.Vote).filter(models.Vote.post_id == post.id).count()
        )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")

@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db), get_current_user: models.User = Depends(oauth2.get_current_user)):
    deleted_post = db.query(models.Post).filter(models.Post.id == id).first()
    # cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    if deleted_post:
        if deleted_post.user_id != get_current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
        db.delete(deleted_post)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")

@router.put("/{id}", response_model=schemas.ReturnPost)
async def update_post(id: int, post: schemas.Post, db: Session = Depends(get_db), get_current_user: models.User = Depends(oauth2.get_current_user)):
    updated_post = db.query(models.Post).filter(models.Post.id == id).first()
    if updated_post:
        if updated_post.user_id != get_current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
        updated_post.title = post.title
        updated_post.content = post.content
        updated_post.published = post.published
        db.commit()
        db.refresh(updated_post)
        return updated_post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
