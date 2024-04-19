import faker
from pathlib import Path


fake = faker.Faker()

path_dir = Path(r".\data")
path_dir.mkdir()
keywords = ["Python", "project", "data", "analysis", "research"]
num_files = 50
for i in range(num_files):
    file_name = f"file_{i+1}.txt"
    file_path = path_dir / file_name
    with open(file_path, "w") as file:
        for j in range(10000):
            if fake.random.choice([True, False]):
                # Choose a random keyword and include it in a random sentence
                sentence = (
                    fake.sentence()
                    + " "
                    + fake.random.choice(keywords)
                    + " "
                    + fake.sentence()
                )
            else:
                sentence = fake.sentence()
            file.write(sentence + "\n")
