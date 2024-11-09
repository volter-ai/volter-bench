import { useCurrentButtons } from "@/lib/useChoices"
import { ArrowLeft, RefreshCw } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card"
import { SkillButton } from "@/components/ui/custom/skill/skill_button"
import { PlayerCard } from "@/components/ui/custom/player/player_card"
import { Button } from "@/components/ui/button"

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
    prototype_id: string
  }
}

interface Creature {
  __type: "Creature"
  uid: string
  display_name: string
  stats: {
    hp: number
    max_hp: number
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
  meta: {
    prototype_id: string
  }
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

export function MainGameSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons()
  const { player, bot } = props.data.entities

  const renderActionButtons = () => {
    if (availableButtonSlugs.includes('back')) {
      return (
        <Button 
          onClick={() => emitButtonClick('back')}
          className="flex items-center gap-2"
        >
          <ArrowLeft className="w-4 h-4" /> Back
        </Button>
      )
    }

    if (availableButtonSlugs.includes('swap')) {
      return (
        <Button
          onClick={() => emitButtonClick('swap')}
          className="flex items-center gap-2"
        >
          <RefreshCw className="w-4 h-4" /> Swap Creature
        </Button>
      )
    }

    return null
  }

  const renderSkillButtons = () => {
    if (!availableButtonSlugs.includes('attack')) return null
    
    return player?.entities?.active_creature?.collections?.skills?.map((skill) => (
      <SkillButton
        key={skill.uid}
        uid={skill.uid}
        skillName={skill.display_name}
        description={skill.description}
        stats={{
          damage: skill.stats.base_damage,
          type: skill.meta.skill_type
        }}
        onClick={() => emitButtonClick('attack', { skillId: skill.uid })}
      />
    ))
  }

  return (
    <div className="h-screen w-screen aspect-[16/9] flex flex-col bg-gradient-to-b from-sky-100 to-sky-50">
      {/* Battlefield Area */}
      <div className="h-2/3 grid grid-cols-2 gap-4 p-4">
        {/* Top Left - Opponent Status */}
        <div className="flex justify-start items-start">
          {bot?.entities?.active_creature && (
            <CreatureCard
              uid={bot.entities.active_creature.uid}
              name={bot.entities.active_creature.display_name}
              hp={bot.entities.active_creature.stats.hp}
              maxHp={bot.entities.active_creature.stats.max_hp}
              imageUrl={`/assets/creatures/${bot.entities.active_creature.meta.prototype_id}/front.png`}
            />
          )}
        </div>

        {/* Top Right - Opponent */}
        <div className="flex justify-end items-start">
          {bot && (
            <PlayerCard
              uid={bot.uid}
              name={bot.display_name}
              imageUrl={`/assets/players/${bot.meta.prototype_id}/avatar.png`}
            />
          )}
        </div>

        {/* Bottom Left - Player */}
        <div className="flex justify-start items-end">
          {player && (
            <PlayerCard
              uid={player.uid}
              name={player.display_name}
              imageUrl={`/assets/players/${player.meta.prototype_id}/avatar.png`}
            />
          )}
        </div>

        {/* Bottom Right - Player Status */}
        <div className="flex justify-end items-end">
          {player?.entities?.active_creature && (
            <CreatureCard
              uid={player.entities.active_creature.uid}
              name={player.entities.active_creature.display_name}
              hp={player.entities.active_creature.stats.hp}
              maxHp={player.entities.active_creature.stats.max_hp}
              imageUrl={`/assets/creatures/${player.entities.active_creature.meta.prototype_id}/back.png`}
            />
          )}
        </div>
      </div>

      {/* UI Area */}
      <div className="h-1/3 p-4 bg-white/80 backdrop-blur-sm">
        <div className="grid grid-cols-2 grid-rows-2 gap-4 h-full">
          {renderSkillButtons()}
          <div className="col-span-2 flex justify-center">
            {renderActionButtons()}
          </div>
        </div>
      </div>
    </div>
  )
}
