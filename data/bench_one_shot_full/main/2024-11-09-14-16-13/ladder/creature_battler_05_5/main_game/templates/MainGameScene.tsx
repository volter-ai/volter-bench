import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, ArrowLeft, SwapHorizontal } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card"
import { PlayerCard } from "@/components/ui/custom/player/player_card"
import { SkillButton } from "@/components/ui/custom/skill/skill_button"
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
    image_front?: string
    image_back?: string
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
    image?: string
  }
  entities: {
    active_creature?: Creature
  }
}

interface GameUIData {
  uid: string
  entities: {
    player: Player
    bot: Player
  }
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const playerCreature = props.data.entities.player?.entities.active_creature
  const botCreature = props.data.entities.bot?.entities.active_creature
  const player = props.data.entities.player
  const bot = props.data.entities.bot

  if (!playerCreature || !botCreature || !player || !bot) {
    return <div uid={`${props.data.uid}-loading`} className="text-center p-4">Loading battle...</div>
  }

  return (
    <div uid={`${props.data.uid}-container`} className="h-screen w-full flex flex-col bg-slate-100">
      {/* Battlefield Area */}
      <div uid={`${props.data.uid}-battlefield`} className="h-2/3 grid grid-cols-2 grid-rows-2 gap-4 p-4">
        {/* Top Left - Opponent Status */}
        <div uid={`${props.data.uid}-opponent-status`} className="flex items-center justify-center">
          <PlayerCard
            uid={bot.uid}
            name={bot.display_name}
            imageUrl={bot.meta.image || '/placeholder.png'}
          />
        </div>

        {/* Top Right - Opponent Creature */}
        <div uid={`${props.data.uid}-opponent-creature`} className="flex items-center justify-center">
          <CreatureCard
            uid={botCreature.uid}
            name={botCreature.display_name}
            hp={botCreature.stats.hp}
            maxHp={botCreature.stats.max_hp}
            imageUrl={botCreature.meta.image_front || '/placeholder.png'}
          />
        </div>

        {/* Bottom Left - Player Creature */}
        <div uid={`${props.data.uid}-player-creature`} className="flex items-center justify-center">
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            hp={playerCreature.stats.hp}
            maxHp={playerCreature.stats.max_hp}
            imageUrl={playerCreature.meta.image_back || '/placeholder.png'}
          />
        </div>

        {/* Bottom Right - Player Status */}
        <div uid={`${props.data.uid}-player-status`} className="flex items-center justify-center">
          <PlayerCard
            uid={player.uid}
            name={player.display_name}
            imageUrl={player.meta.image || '/placeholder.png'}
          />
        </div>
      </div>

      {/* UI Area */}
      <div uid={`${props.data.uid}-ui`} className="h-1/3 p-4 bg-white rounded-t-xl shadow-lg">
        <div uid={`${props.data.uid}-buttons`} className="grid grid-cols-2 gap-4 h-full">
          {availableButtonSlugs.includes('attack') && playerCreature.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={{
                damage: skill.stats.base_damage,
                type: skill.meta.skill_type
              }}
            />
          ))}
          
          {availableButtonSlugs.includes('back') && (
            <Button 
              uid={`${props.data.uid}-back-button`}
              className="flex items-center gap-2"
            >
              <ArrowLeft className="w-4 h-4" /> Back
            </Button>
          )}
          
          {availableButtonSlugs.includes('swap') && (
            <Button 
              uid={`${props.data.uid}-swap-button`}
              className="flex items-center gap-2"
            >
              <SwapHorizontal className="w-4 h-4" /> Swap
            </Button>
          )}
        </div>
      </div>
    </div>
  )
}
