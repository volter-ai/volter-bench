import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Shield, Swords } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card"
import { SkillButton } from "@/components/ui/custom/skill/skill_button"
import { PlayerCard } from "@/components/ui/custom/player/player_card"

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
  }
  collections: {
    skills: Skill[]
  }
}

interface Player {
  __type: "Player"
  uid: string
  display_name: string
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
    availableButtonSlugs = [],
    emitButtonClick
  } = useCurrentButtons()

  const playerCreature = props.data.entities.player_creature
  const botCreature = props.data.entities.bot_creature
  const player = props.data.entities.player
  const bot = props.data.entities.bot

  return (
    <div className="h-screen w-screen flex flex-col bg-background">
      {/* HUD */}
      <nav className="h-[10%] bg-secondary flex items-center justify-between px-6 border-b">
        {player && (
          <PlayerCard
            uid={player.uid}
            name={player.display_name}
            imageUrl={`/players/${player.uid}.png`}
            className="w-[200px] h-[80px]"
          />
        )}
        {bot && (
          <PlayerCard
            uid={bot.uid}
            name={bot.display_name}
            imageUrl={`/players/${bot.uid}.png`}
            className="w-[200px] h-[80px]"
          />
        )}
      </nav>

      {/* Battlefield */}
      <div className="h-[60%] flex justify-between items-center px-12 relative">
        {playerCreature && (
          <div className="relative">
            <span className="absolute -top-8 left-1/2 -translate-x-1/2 text-sm font-bold">
              Your Creature
            </span>
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              currentHp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
              imageUrl={`/creatures/${playerCreature.uid}.png`}
            />
          </div>
        )}

        {botCreature && (
          <div className="relative">
            <span className="absolute -top-8 left-1/2 -translate-x-1/2 text-sm font-bold">
              Opponent's Creature
            </span>
            <CreatureCard
              uid={botCreature.uid}
              name={botCreature.display_name}
              currentHp={botCreature.stats.hp}
              maxHp={botCreature.stats.max_hp}
              imageUrl={`/creatures/${botCreature.uid}.png`}
            />
          </div>
        )}
      </div>

      {/* Controls */}
      <div className="h-[30%] bg-secondary rounded-t-xl p-6">
        <div className="grid grid-cols-2 gap-4 max-w-[600px] mx-auto">
          {playerCreature?.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={{
                damage: skill.stats.base_damage
              }}
              onClick={() => availableButtonSlugs.includes(skill.uid) && emitButtonClick(skill.uid)}
              disabled={!availableButtonSlugs.includes(skill.uid)}
            />
          ))}
        </div>
      </div>
    </div>
  )
}
