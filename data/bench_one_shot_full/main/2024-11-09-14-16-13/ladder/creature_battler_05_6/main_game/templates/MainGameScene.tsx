import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, SwapHorizontal } from 'lucide-react'
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
  entities: {
    active_creature?: Creature
  }
}

interface GameUIData {
  entities: {
    player: Player
    bot: Player
  }
}

const isCreature = (entity: any): entity is Creature => 
  entity?.__type === "Creature"

const isSkill = (entity: any): entity is Skill => 
  entity?.__type === "Skill"

const isPlayer = (entity: any): entity is Player => 
  entity?.__type === "Player"

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const player = props.data.entities.player
  const bot = props.data.entities.bot
  
  if (!isPlayer(player) || !isPlayer(bot)) {
    return <div className="w-full h-full flex items-center justify-center">
      Invalid player data
    </div>
  }

  const playerCreature = player.entities.active_creature
  const botCreature = bot.entities.active_creature

  if (!isCreature(playerCreature) || !isCreature(botCreature)) {
    return <div className="w-full h-full flex items-center justify-center">
      Invalid creature data
    </div>
  }

  return (
    <div className="w-full h-full flex flex-col">
      {/* Battlefield Area (upper 2/3) */}
      <div className="h-2/3 grid grid-cols-2 grid-rows-2 gap-4 p-4 bg-slate-100">
        {/* Top Left - Opponent Status */}
        <div className="flex items-center justify-start">
          <PlayerCard
            uid={bot.uid}
            name={bot.display_name}
            imageUrl={`/players/${bot.display_name.toLowerCase()}.png`}
          />
          <CreatureCard
            uid={botCreature.uid}
            name={botCreature.display_name}
            image={`/creatures/${botCreature.display_name.toLowerCase()}_front.png`}
            currentHp={botCreature.stats.hp}
            maxHp={botCreature.stats.max_hp}
          />
        </div>

        {/* Top Right - Opponent Creature */}
        <div className="flex items-center justify-center">
          <div className="relative">
            <img
              src={`/creatures/${botCreature.display_name.toLowerCase()}_front.png`}
              alt={botCreature.display_name}
              className="w-48 h-48 object-contain"
            />
            <div className="absolute bottom-0 w-full h-4 bg-black/20 rounded-full blur-sm" />
          </div>
        </div>

        {/* Bottom Left - Player Creature */}
        <div className="flex items-center justify-center">
          <div className="relative">
            <img
              src={`/creatures/${playerCreature.display_name.toLowerCase()}_back.png`}
              alt={playerCreature.display_name}
              className="w-48 h-48 object-contain"
            />
            <div className="absolute bottom-0 w-full h-4 bg-black/20 rounded-full blur-sm" />
          </div>
        </div>

        {/* Bottom Right - Player Status */}
        <div className="flex items-center justify-end">
          <PlayerCard
            uid={player.uid}
            name={player.display_name}
            imageUrl={`/players/${player.display_name.toLowerCase()}.png`}
          />
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            image={`/creatures/${playerCreature.display_name.toLowerCase()}_back.png`}
            currentHp={playerCreature.stats.hp}
            maxHp={playerCreature.stats.max_hp}
          />
        </div>
      </div>

      {/* UI Area (lower 1/3) */}
      <div className="h-1/3 p-4 bg-white">
        <div className="grid grid-cols-2 gap-4 h-full">
          {availableButtonSlugs.map(slug => {
            if (slug === 'attack') {
              return playerCreature.collections.skills.filter(isSkill).map((skill) => (
                <SkillButton
                  key={skill.uid}
                  uid={skill.uid}
                  name={skill.display_name}
                  description={skill.description}
                  stats={{
                    damage: skill.stats.base_damage
                  }}
                  onClick={() => emitButtonClick('attack')}
                />
              ));
            }
            if (slug === 'swap') {
              return (
                <SkillButton
                  key="swap-button"
                  uid="swap-button"
                  name="Swap Creature"
                  description="Switch to a different creature"
                  stats={{}}
                  onClick={() => emitButtonClick('swap')}
                />
              );
            }
            return null;
          })}
        </div>
      </div>
    </div>
  )
}
