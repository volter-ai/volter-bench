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
  meta: {
    prototype_id: string
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
  meta: {
    prototype_id: string
  }
  collections: {
    skills: Skill[]
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
    player_creature: Creature
    bot_creature: Creature
  }
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const playerCreature = props.data.entities.player_creature
  const botCreature = props.data.entities.bot_creature

  const getCreatureImageUrl = (creature?: Creature) => {
    return creature?.meta?.prototype_id 
      ? `/creatures/${creature.meta.prototype_id}.png`
      : '/creatures/default.png'
  }

  return (
    <div className="flex flex-col h-screen w-full bg-background">
      {/* HUD */}
      <div className="h-1/6 flex items-center justify-between px-6 border-b">
        <div className="flex items-center gap-4">
          <Sword className="h-6 w-6" />
          <span>Battle Scene</span>
        </div>
        <div className="flex items-center gap-4">
          <Shield className="h-6 w-6" />
          <Zap className="h-6 w-6" />
        </div>
      </div>

      {/* Battlefield */}
      <div className="h-3/6 flex items-center justify-between px-12">
        {playerCreature && (
          <div className="relative">
            <div className="absolute -top-8 left-1/2 -translate-x-1/2 bg-primary text-primary-foreground px-3 py-1 rounded-full text-sm">
              Player
            </div>
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              currentHp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
              imageUrl={getCreatureImageUrl(playerCreature)}
            />
          </div>
        )}

        {botCreature && (
          <div className="relative">
            <div className="absolute -top-8 left-1/2 -translate-x-1/2 bg-destructive text-destructive-foreground px-3 py-1 rounded-full text-sm">
              Opponent
            </div>
            <CreatureCard
              uid={botCreature.uid}
              name={botCreature.display_name}
              currentHp={botCreature.stats.hp}
              maxHp={botCreature.stats.max_hp}
              imageUrl={getCreatureImageUrl(botCreature)}
            />
          </div>
        )}
      </div>

      {/* Skills/UI Area */}
      <div className="h-2/6 bg-muted p-6">
        <div className="grid grid-cols-2 gap-4 h-full">
          {playerCreature?.collections.skills
            .filter(skill => availableButtonSlugs.includes(skill.uid))
            .map((skill) => (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                name={skill.display_name}
                description={skill.description}
                stats={{
                  damage: skill.stats.base_damage
                }}
                onClick={() => emitButtonClick(skill.uid)}
              />
            ))}
        </div>
      </div>
    </div>
  )
}
