from core.agent_runner import generate_agent_id

def test_generate_agent_id_format():
    agent_id = generate_agent_id("cursor-gpt4")
    parts = agent_id.split("--")
    assert len(parts) == 2
    meta = parts[0].split("-")
    # cursor-gpt4-v1-YYYYMMDD
    assert meta[0] == "cursor"
    assert meta[1].startswith("gpt4")