import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Shield, Swords } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card"
import { SkillButton } from "@/components/ui/custom/skill/skill_button"

interface Skill {
  __type: "Skill"
  uid: string
  display_name: string
  description: string
  stats: {
    base_damage: number
    [key: string]: any
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

  if (!playerCreature || !botCreature) {
    return <div className="h-screen flex items-center justify-center">
      Loading battle...
    </div>
  }

  return (
    <div className="h-screen w-full flex flex-col">
      {/* Top HUD */}
      <nav className="h-[10vh] bg-secondary flex items-center justify-between px-4">
        <div className="flex items-center gap-2">
          <Shield className="h-5 w-5" />
          <span>Player: {props.data.entities.player?.display_name ?? 'Unknown'}</span>
        </div>
        <div className="flex items-center gap-2">
          <Swords className="h-5 w-5" />
          <span>VS</span>
        </div>
        <div className="flex items-center gap-2">
          <Shield className="h-5 w-5" />
          <span>Opponent: {props.data.entities.bot?.display_name ?? 'Unknown'}</span>
        </div>
      </nav>

      {/* Battlefield */}
      <div className="h-[50vh] flex items-center justify-between px-16 bg-background">
        <div className="relative">
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            currentHp={playerCreature.stats.hp}
            maxHp={playerCreature.stats.max_hp}
            imageUrl={playerCreature.meta?.prototype_id ? 
              `/creatures/${playerCreature.meta.prototype_id}.png` : 
              '/creatures/default.png'
            }
            className="transform hover:scale-105 transition-transform"
          />
          <div className="absolute -bottom-6 left-1/2 -translate-x-1/2 bg-primary text-primary-foreground px-3 py-1 rounded-full text-sm">
            Your Creature
          </div>
        </div>

        <div className="relative">
          <CreatureCard
            uid={botCreature.uid}
            name={botCreature.display_name}
            currentHp={botCreature.stats.hp}
            maxHp={botCreature.stats.max_hp}
            imageUrl={botCreature.meta?.prototype_id ? 
              `/creatures/${botCreature.meta.prototype_id}.png` : 
              '/creatures/default.png'
            }
            className="transform hover:scale-105 transition-transform"
          />
          <div className="absolute -bottom-6 left-1/2 -translate-x-1/2 bg-destructive text-destructive-foreground px-3 py-1 rounded-full text-sm">
            Opponent
          </div>
        </div>
      </div>

      {/* Control Area */}
      <div className="h-[40vh] bg-secondary/50 p-6 rounded-t-xl">
        <div className="bg-background rounded-lg p-4 h-full">
          <h3 className="text-lg font-bold mb-4">Available Actions</h3>
          <div className="grid grid-cols-2 gap-4">
            {playerCreature.collections?.skills?.map((skill) => (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                skillName={skill.display_name}
                description={skill.description}
                stats={skill.stats}
              />
            )) ?? (
              <div className="col-span-2 text-center text-muted-foreground">
                No skills available
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
