import numpy as np
import pytest
import model

def test_real_training_and_inference():
    fitted,accuracy=model.train_model()
    assert 0 <= accuracy <= 1
    record=model.load_data().iloc[0][model.FEATURES].to_dict()
    label,score=model.predict(fitted,record)
    assert label in (0,1) and 0 <= score <= 1
def test_bad_input():
    with pytest.raises(ValueError):model.predict(None,{})
    record={key:0 for key in model.FEATURES};record['age']=np.nan
    with pytest.raises(ValueError):model.predict(None,record)
