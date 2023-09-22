import random
import multiprocessing
from tqdm import tqdm
from datetime import datetime

dt = datetime.now()

# 랜덤 시드
random.seed(dt.microsecond)

# 유전자 변이 확률
mutation_rate = 0.1

# 초기 유전자
initial_gene = [0, 0]

def seeding():
    global dt
    dt = datetime.now()
    # 랜덤 시드
    random.seed(dt.microsecond)
    
def mutate(gene):
    seeding()
    """주어진 확률로 유전자 변이"""
    return [1 if random.random() < mutation_rate else g for g in gene]

def breed(parents):
    seeding()
    """부모로부터 자손 생성"""
    child_gene = [random.choice([parents[0][i], parents[1][i]]) for i in range(2)]
    return mutate(child_gene)

def create_generation(num_pairs):
    """새로운 세대 생성"""
    generation = [[initial_gene.copy(), initial_gene.copy()] for _ in range(num_pairs)]
    
    # 교배를 통해 다음 세대 생성
    next_generation = []
    
    for i, parents in enumerate(generation):
        child = breed(parents)
        next_generation.append((child, i))  # 자식 유전자와 부모 인덱스 저장
        
    return next_generation

def count_genes(generation):
   """세대 내에서 유전자의 수를 세는 함수"""
   
   zero_one, one_one, two_one = 0, 0, 0
   
   for gene in generation:
       ones_count = gene.count(1)
       if ones_count == 0:
           zero_one += 1
       elif ones_count == 1:
           one_one += 1
       elif ones_count ==2 :
           two_one +=1
   
   return zero_one, one_one, two_one


# 각각의 뭉치에 대한 시뮬레이션 실행
num_pairs = 100 # 예시로 사용할 부모 쌍의 수

def simulate(i): 
    # 무작위 교배 뭉치
    random_bunch=create_generation(num_pairs) 
   
    # 사촌 교배 그룹
    incest_bunch=[]
   
    for j in range(num_pairs//4):
        seeding()
        incest_bunch.append(breed([random_bunch[j*4], random_bunch[j*4+1]]))
        incest_bunch.append(breed([random_bunch[(j*4+2)%num_pairs], random_bunch[(j*4+3)%num_pairs]]))
        incest_bunch.append(breed([random_bunch[(j*4+4)%num_pairs], random_bunch[(j*4+5)%num_pairs]]))
        incest_bunch.append(breed([random_bunch[(j*4+6)%num_pairs], random_bunch[(j*4+7)%num_pairs]]))

    # 사촌 외 교배 그룹
    non_incest_bunch=[]
   
    # 모든 가능한 짝을 만들기
    pairs = [(i, j) for i in range(len(random_bunch)) for j in range(i+1, len(random_bunch))]
   
    # 사촌이 아닌 짝만 선택하기 (부모가 다른 경우)
    non_incest_pairs = [(i,j) for i,j in pairs if random_bunch[i][1] != random_bunch[j][1]]
   
    if non_incest_pairs:  # 비어있지 않은 경우에만 처리하기
        for _ in range(num_pairs):
            pair_index=random.choice(non_incest_pairs)
            non_incest_parents=[random_bunch[pair_index[0]][0],random_bunch[pair_index[1]][0]]
            non_incest_child=breed(non_incest_parents)
            non_incest_bunch.append(non_incest_child)
       
    else:  # 모든 개체가 동일한 부모 쌍으로부터 생성된 경우
        for _ in range(num_pairs):
            pair_index=random.choice(pairs)  # 무작위로 두 개체 선택하기
            random_parents=[random_bunch[pair_index[0]][0],random_bunch[pair_index[1]][0]]
            random_child=breed(random_parents)
            non_incest_bunch.append(random_child)
    


    return count_genes(random_bunch), count_genes(incest_bunch), count_genes(non_incest_bunch)

gencount = 10000

if __name__ == "__main__":
    with multiprocessing.Pool() as pool:
        results = list(tqdm(pool.imap_unordered(simulate, range(gencount)), total=gencount))
        results_random_bunc, results_incest_bunc, results_non_inc = zip(*results)

    print("근친혼 그룹")
    zero_ones_incest, one_ones_incest,two_ones_incest= zip(*results_incest_bunc)
    print(f"이상 유전자 0개: {sum(zero_ones_incest)}, 이상 유전자 1개:{sum(one_ones_incest)}, 이상 유전자 2개:{sum(two_ones_incest)}")
    print()
    print("근친혼 금지 그룹")
    zeroOnesNonInc ,oneOneNonInc,twoOneNonInc= zip(*results_non_inc)
    print(f"이상 유전자 0개: {sum(zeroOnesNonInc)}, 이상 유전자 1개:{sum(oneOneNonInc)}, 이상 유전자 2개:{sum(twoOneNonInc)}")

