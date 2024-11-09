import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield, Zap } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card"
import { SkillButton } from "@/components/ui/custom/skill/skill_button"

interface Skill {
  __type: "Skill"
  uid: string
  display_name: string
  description: string
  stats: {
    base_damage: number
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
    speed: number
  }
  collections: {
    skills?: Skill[]
  }
  meta: {
    prototype_id?: string
  }
}

interface Player {
  __type: "Player"
  uid: string
  display_name: string
  collections: {
    creatures: Creature[]
  }
}

interface GameUIData {
  entities: {
    player: Player
    bot: Player
    player_creature?: Creature
    bot_creature?: Creature
  }
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const playerCreature = props.data.entities.player_creature
  const botCreature = props.data.entities.bot_creature

  const renderStats = (creature?: Creature) => {
    if (!creature) return null
    
    return (
      <div className="flex items-center gap-4">
        <Sword className="h-6 w-6" />
        <span>{creature.stats?.attack ?? 0}</span>
        <Shield className="h-6 w-6" />
        <span>{creature.stats?.defense ?? 0}</span>
        <Zap className="h-6 w-6" />
        <span>{creature.stats?.speed ?? 0}</span>
      </div>
    )
  }

  const renderCreature = (creature?: Creature, label?: string) => {
    if (!creature) return null

    return (
      <div className="relative">
        {label && (
          <span className="absolute -top-8 left-1/2 -translate-x-1/2 text-sm font-bold">
            {label}
          </span>
        )}
        <CreatureCard
          uid={creature.uid}
          name={creature.display_name}
          currentHp={creature.stats?.hp ?? 0}
          maxHp={creature.stats?.max_hp ?? 0}
          imageUrl={creature.meta?.prototype_id ? 
            `/creatures/${creature.meta.prototype_id}.png` : 
            '/creatures/default.png'
          }
        />
      </div>
    )
  }

  const renderSkills = (creature?: Creature) => {
    if (!creature?.collections?.skills?.length) return null

    return (
      <div className="grid grid-cols-2 gap-4">
        {creature.collections.skills.map((skill) => (
          <SkillButton
            key={skill.uid}
            uid={skill.uid}
            name={skill.display_name}
            description={skill.description}
            stats={{
              damage: skill.stats?.base_damage
            }}
          />
        ))}
      </div>
    )
  }

  return (
    <div className="w-full h-full aspect-video flex flex-col">
      {/* HUD */}
      <div className="h-1/8 bg-secondary p-4 flex justify-between items-center">
        {renderStats(playerCreature)}
      </div>

      {/* Battlefield */}
      <div className="flex-1 flex justify-between items-center px-16 bg-primary/10">
        {renderCreature(playerCreature, "Your Creature")}
        {renderCreature(botCreature, "Opponent's Creature")}
      </div>

      {/* Skills Area */}
      <div className="h-3/8 bg-secondary p-4">
        {renderSkills(playerCreature)}
      </div>
    </div>
  )
}
