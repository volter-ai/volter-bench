import { useCurrentButtons } from "@/lib/useChoices.ts";
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

  const { player, opponent, player_creature, opponent_creature } = props.data.entities

  if (!player || !opponent || !player_creature || !opponent_creature) {
    return <div className="h-full w-full flex items-center justify-center">Loading...</div>
  }

  const handleSkillClick = (skillUid: string) => {
    // Ensure we're only emitting valid button slugs
    const matchingSkill = player_creature.collections.skills.find(
      skill => skill.uid === skillUid && availableButtonSlugs.includes(skillUid)
    )
    if (matchingSkill) {
      emitButtonClick(skillUid)
    }
  }

  // Ensure we have both skills and available buttons before filtering
  const availableSkills = Array.isArray(availableButtonSlugs) && availableButtonSlugs.length > 0
    ? player_creature.collections.skills.filter(skill => availableButtonSlugs.includes(skill.uid))
    : []

  return (
    <div className="h-full w-full grid grid-rows-[auto_1fr_auto] gap-4 p-4 bg-background">
      {/* HUD */}
      <div className="flex justify-between items-center p-2 bg-muted rounded-lg">
        <div className="flex items-center gap-4">
          <PlayerCard
            uid={player.uid}
            name={player.display_name}
            imageUrl=""
          />
          <div className="text-sm font-medium">
            {player_creature.display_name}
          </div>
        </div>
        <div className="flex items-center gap-4">
          <div className="text-sm font-medium">
            {opponent_creature.display_name}
          </div>
          <PlayerCard
            uid={opponent.uid}
            name={opponent.display_name}
            imageUrl=""
          />
        </div>
      </div>

      {/* Battlefield */}
      <div className="flex justify-between items-center px-12">
        <CreatureCard
          uid={player_creature.uid}
          name={player_creature.display_name}
          currentHp={player_creature.stats.hp}
          maxHp={player_creature.stats.max_hp}
          imageUrl=""
        />
        
        <CreatureCard
          uid={opponent_creature.uid}
          name={opponent_creature.display_name}
          currentHp={opponent_creature.stats.hp}
          maxHp={opponent_creature.stats.max_hp}
          imageUrl=""
        />
      </div>

      {/* Skills UI */}
      <div className="bg-muted p-4 rounded-lg min-h-[120px]">
        <div className="grid grid-cols-2 gap-4">
          {availableSkills.length > 0 ? (
            availableSkills.map((skill) => (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                name={skill.display_name}
                description={skill.description}
                damage={skill.stats.base_damage}
                onClick={() => handleSkillClick(skill.uid)}
              />
            ))
          ) : (
            <div className="col-span-2 text-center text-muted-foreground">
              Waiting for available actions...
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
