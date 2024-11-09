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
    category: string
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
    category: string
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
    bot: Player
    player_creature: Creature
    bot_creature: Creature
  }
  meta: Record<string, unknown>
  stats: Record<string, unknown>
  collections: Record<string, unknown>
  uid: string
  display_name: string
  description: string
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const playerCreature = props.data?.entities?.player_creature
  const botCreature = props.data?.entities?.bot_creature

  if (!playerCreature || !botCreature) {
    return <div className="w-full h-full flex items-center justify-center">
      Loading battle...
    </div>
  }

  return (
    <div className="w-full h-full flex flex-col bg-background">
      {/* HUD */}
      <div className="w-full h-16 bg-secondary/10 border-b flex items-center px-4">
        <div className="flex items-center gap-4">
          <Sword className="h-5 w-5" />
          <Shield className="h-5 w-5" />
          <Zap className="h-5 w-5" />
        </div>
      </div>

      {/* Battlefield */}
      <div className="flex-1 flex items-center justify-between px-16 py-8">
        <div className="relative">
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            currentHp={playerCreature.stats.hp}
            maxHp={playerCreature.stats.max_hp}
            imageUrl={`/creatures/${playerCreature.meta.prototype_id}.png`}
            className="transform scale-110"
          />
          <div className="absolute -bottom-6 left-1/2 -translate-x-1/2 bg-primary/10 px-3 py-1 rounded-full text-sm">
            Player
          </div>
        </div>

        <div className="relative">
          <CreatureCard
            uid={botCreature.uid}
            name={botCreature.display_name}
            currentHp={botCreature.stats.hp}
            maxHp={botCreature.stats.max_hp}
            imageUrl={`/creatures/${botCreature.meta.prototype_id}.png`}
            className="transform scale-110"
          />
          <div className="absolute -bottom-6 left-1/2 -translate-x-1/2 bg-destructive/10 px-3 py-1 rounded-full text-sm">
            Opponent
          </div>
        </div>
      </div>

      {/* Action UI */}
      <div className="h-48 bg-secondary/5 border-t p-4">
        <div className="grid grid-cols-2 gap-4 h-full">
          {playerCreature.collections?.skills?.length > 0 ? (
            playerCreature.collections.skills.map((skill) => (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                name={skill.display_name}
                description={skill.description}
                stats={{
                  damage: skill.stats.base_damage
                }}
              />
            ))
          ) : (
            <div className="col-span-2 flex items-center justify-center text-muted-foreground">
              No skills available
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
