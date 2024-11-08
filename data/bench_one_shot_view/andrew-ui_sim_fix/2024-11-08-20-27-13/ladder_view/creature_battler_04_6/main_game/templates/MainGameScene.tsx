import { useCurrentButtons } from "@/lib/useChoices"
import { Heart } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card"
import { SkillButton } from "@/components/ui/custom/skill/skill_button"
import { Progress } from "@/components/ui/progress"
import { Card, CardContent, CardHeader } from "@/components/ui/card"

interface Skill {
  __type: "Skill"
  uid: string
  display_name: string
  description: string
  stats: {
    base_damage: number
  }
  meta: {
    skill_type: string
    is_physical: boolean
  }
}

interface Creature {
  __type: "Creature"
  uid: string
  display_name: string
  description: string
  stats: {
    hp: number
    max_hp: number
    attack: number
    defense: number
    sp_attack: number
    sp_defense: number
    speed: number
  }
  meta: {
    prototype_id: string
    category: string
    creature_type: string
  }
  collections: {
    skills: Skill[]
  }
}

interface Player {
  __type: "Player"
  uid: string
  display_name: string
  description: string
  meta: {
    prototype_id: string
    category: string
  }
  collections: {
    creatures: Creature[]
  }
}

interface GameUIData {
  entities: {
    player: Player
    opponent: Player
    player_creature: Creature
    opponent_creature: Creature
  }
}

function CreatureStatus({ creature }: { creature: Creature }) {
  return (
    <Card className="w-[250px]">
      <CardHeader className="pb-2">
        <h3 className="font-bold flex items-center gap-2">
          <Heart className="w-4 h-4" />
          {creature.display_name}
        </h3>
      </CardHeader>
      <CardContent>
        <div className="space-y-2">
          <div className="flex justify-between text-sm">
            <span>HP</span>
            <span>{creature.stats.hp}/{creature.stats.max_hp}</span>
          </div>
          <Progress 
            value={(creature.stats.hp / creature.stats.max_hp) * 100} 
          />
        </div>
      </CardContent>
    </Card>
  )
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const playerCreature = props.data.entities.player_creature
  const opponentCreature = props.data.entities.opponent_creature

  if (!playerCreature || !opponentCreature) {
    return <div>Loading...</div>
  }

  return (
    <div className="h-screen w-screen aspect-[16/9] bg-slate-100">
      {/* Battlefield */}
      <div className="h-2/3 grid grid-cols-2 p-4 gap-4">
        {/* Top Row */}
        <div className="flex justify-start items-start">
          <CreatureStatus creature={opponentCreature} />
        </div>
        
        <div className="flex justify-end items-start">
          <CreatureCard
            uid={opponentCreature.uid}
            name={opponentCreature.display_name}
            imageUrl={`/creatures/${opponentCreature.meta.prototype_id}_front.png`}
            currentHp={opponentCreature.stats.hp}
            maxHp={opponentCreature.stats.max_hp}
          />
        </div>

        {/* Bottom Row */}
        <div className="flex justify-start items-end">
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            imageUrl={`/creatures/${playerCreature.meta.prototype_id}_back.png`}
            currentHp={playerCreature.stats.hp}
            maxHp={playerCreature.stats.max_hp}
          />
        </div>

        <div className="flex justify-end items-end">
          <CreatureStatus creature={playerCreature} />
        </div>
      </div>

      {/* UI Section */}
      <div className="h-1/3 grid grid-cols-2 gap-4 p-4">
        {playerCreature.collections?.skills?.map((skill: Skill) => (
          <SkillButton
            key={skill.uid}
            uid={skill.uid}
            skillName={skill.display_name}
            description={skill.description}
            damage={skill.stats.base_damage}
            type={skill.meta.skill_type}
          />
        )) ?? <div>No skills available</div>}
      </div>
    </div>
  )
}
