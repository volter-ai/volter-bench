import { useCurrentButtons } from "@/lib/useChoices.ts";
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
  }
  meta: {
    skill_type: string
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
  meta: {
    creature_type: string
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
    opponent: Player
    player_creature: Creature
    opponent_creature: Creature
  }
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const playerCreature = props.data.entities.player_creature
  const opponentCreature = props.data.entities.opponent_creature
  const player = props.data.entities.player
  const opponent = props.data.entities.opponent

  const getCreatureImageUrl = (creature: Creature) => 
    `/assets/creatures/${creature.meta.creature_type}/${creature.uid}.png`
  
  const getPlayerImageUrl = (player: Player) =>
    `/assets/players/${player.uid}.png`

  const handleSkillClick = (skillUid: string) => {
    if (availableButtonSlugs?.includes(skillUid)) {
      emitButtonClick(skillUid)
    }
  }

  return (
    <div className="w-full h-full grid grid-rows-6 bg-background">
      {/* HUD */}
      <div className="row-span-1 bg-muted/50 p-4 flex justify-between items-center border-b">
        {player && (
          <PlayerCard
            uid={player.uid}
            name={player.display_name}
            imageUrl={getPlayerImageUrl(player)}
            className="scale-75 -translate-y-6"
          />
        )}
        <div className="flex items-center gap-4">
          <Shield className="h-6 w-6" />
          <span className="text-xl font-bold">VS</span>
          <Swords className="h-6 w-6" />
        </div>
        {opponent && (
          <PlayerCard
            uid={opponent.uid}
            name={opponent.display_name}
            imageUrl={getPlayerImageUrl(opponent)}
            className="scale-75 -translate-y-6"
          />
        )}
      </div>

      {/* Battlefield */}
      <div className="row-span-3 flex justify-between items-center px-16">
        {playerCreature && (
          <div className="relative">
            <span className="absolute -top-8 left-1/2 -translate-x-1/2 text-sm font-bold">
              Your {playerCreature.display_name}
            </span>
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              currentHp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
              imageUrl={getCreatureImageUrl(playerCreature)}
            />
          </div>
        )}

        {opponentCreature && (
          <div className="relative">
            <span className="absolute -top-8 left-1/2 -translate-x-1/2 text-sm font-bold">
              Opponent's {opponentCreature.display_name}
            </span>
            <CreatureCard
              uid={opponentCreature.uid}
              name={opponentCreature.display_name}
              currentHp={opponentCreature.stats.hp}
              maxHp={opponentCreature.stats.max_hp}
              imageUrl={getCreatureImageUrl(opponentCreature)}
            />
          </div>
        )}
      </div>

      {/* UI Area */}
      <div className="row-span-2 bg-muted/30 p-6">
        <div className="h-full flex flex-col">
          <div className="flex-1 bg-background rounded-lg p-4 shadow-inner">
            {playerCreature?.collections.skills && playerCreature.collections.skills.length > 0 ? (
              <div className="h-full grid grid-cols-2 gap-4">
                {playerCreature.collections.skills.map((skill) => {
                  const isAvailable = availableButtonSlugs?.includes(skill.uid)
                  return (
                    <SkillButton
                      key={skill.uid}
                      uid={skill.uid}
                      name={skill.display_name}
                      description={skill.description}
                      damage={skill.stats.base_damage}
                      variant={isAvailable ? "default" : "secondary"}
                      disabled={!isAvailable}
                      onClick={() => handleSkillClick(skill.uid)}
                      aria-label={`Use skill ${skill.display_name}`}
                    />
                  )
                })}
              </div>
            ) : (
              <div className="h-full flex items-center justify-center">
                <p className="text-muted-foreground">No skills available</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
