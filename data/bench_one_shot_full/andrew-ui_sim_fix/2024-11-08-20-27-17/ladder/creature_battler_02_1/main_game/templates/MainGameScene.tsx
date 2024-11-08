import { useCurrentButtons } from "@/lib/useChoices.ts"
import { Shield, Swords } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card"
import { PlayerCard } from "@/components/ui/custom/player/player_card"
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
    image_url?: string
  }
  collections: {
    skills: Skill[]
  }
}

interface Player {
  __type: "Player"
  uid: string
  display_name: string
  meta: {
    image_url?: string
  }
  collections: {
    creatures: Creature[]
  }
}

interface GameUIData {
  entities: {
    player?: Player
    bot?: Player
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
  const player = props.data.entities.player
  const bot = props.data.entities.bot

  if (!player || !bot || !playerCreature || !botCreature) {
    return (
      <div className="h-screen w-full flex items-center justify-center bg-slate-900 text-white">
        Loading battle...
      </div>
    )
  }

  return (
    <div className="h-screen w-full flex flex-col bg-slate-900 text-white">
      {/* HUD */}
      <nav className="w-full p-4 bg-slate-800 flex justify-between items-center">
        <PlayerCard 
          uid={player.uid}
          name={player.display_name}
          imageUrl={player.meta.image_url || "/default/player.png"}
        />
        <PlayerCard 
          uid={bot.uid}
          name={bot.display_name}
          imageUrl={bot.meta.image_url || "/default/opponent.png"}
        />
      </nav>

      {/* Battlefield */}
      <div className="flex-1 flex justify-between items-center px-12">
        <div className="flex flex-col items-center">
          <div className="mb-4 flex items-center">
            <Shield className="mr-2" /> Player
          </div>
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            currentHp={playerCreature.stats.hp}
            maxHp={playerCreature.stats.max_hp}
            imageUrl={playerCreature.meta.image_url || "/default/creature.png"}
          />
        </div>

        <div className="flex flex-col items-center">
          <div className="mb-4 flex items-center">
            <Swords className="mr-2" /> Opponent
          </div>
          <CreatureCard
            uid={botCreature.uid}
            name={botCreature.display_name}
            currentHp={botCreature.stats.hp}
            maxHp={botCreature.stats.max_hp}
            imageUrl={botCreature.meta.image_url || "/default/creature.png"}
          />
        </div>
      </div>

      {/* UI Area */}
      <div className="h-1/3 bg-slate-700 p-4 rounded-t-lg">
        <div className="grid grid-cols-2 gap-4">
          {playerCreature.collections?.skills?.map((skill) => (
            skill && (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                skillName={skill.display_name}
                description={skill.description}
                stats={skill.stats}
              />
            )
          ))}
          {(!playerCreature.collections?.skills || playerCreature.collections.skills.length === 0) && (
            <div className="col-span-2 text-center text-slate-400">
              No skills available
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
