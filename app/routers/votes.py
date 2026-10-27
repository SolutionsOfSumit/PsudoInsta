from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from .. import schemas, db_connection, models, oauth2

router = APIRouter(
    prefix="/vote", 
    tags=["Vote"]
    )

@router.post("/", status_code= status.HTTP_201_CREATED)
def vote(vote:schemas.Vote, db: Session = Depends(db_connection.get_db), current_user : int = Depends(oauth2.get_current_user)):

    vote_query =  db.query(models.Voting).filter(
        models.Voting.post_id == vote.post_id, 
        models.Voting.user_id == current_user.id
    )
    
    found_vote = vote_query.first()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You have already voted on this image")

        new_vote = models.Voting(post_id= vote.post_id, user_id= current_user.id)

        print(new_vote)

        db.add(new_vote)
        db.commit()
        return {"message":"Successfully Created Vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="vote does not exist")
        
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "Successfully Deleted Vote"}

