import * as React from "react"
import { cn } from "@/lib/utils"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import withClickable from "@/lib/withClickable"

interface CreatureCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  hp: number
  maxHp: number
  imageUrl: string
}

let CreatureCardRoot = withClickable(Card)
let CreatureCardHeaderRoot = withClickable(CardHeader)
let CreatureCardTitleRoot = withClickable(CardTitle)
let CreatureCardContentRoot = withClickable(CardContent)

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, hp, maxHp, imageUrl, ...props }, ref) => {
    return (
      <CreatureCardRoot uid={uid} ref={ref} className={cn("w-[300px]", className)} {...props}>
        <CreatureCardHeaderRoot uid={`${uid}-header`}>
          <CreatureCardTitleRoot uid={`${uid}-title`}>{name}</CreatureCardTitleRoot>
        </CreatureCardHeaderRoot>
        <CreatureCardContentRoot uid={`${uid}-content`}>
          <div className="flex flex-col gap-4">
            <img 
              src={imageUrl}
              alt={name}
              className="w-full h-[200px] object-cover rounded-md"
            />
            <div className="flex justify-between items-center">
              <span>HP:</span>
              <span>{hp}/{maxHp}</span>
            </div>
          </div>
        </CreatureCardContentRoot>
      </CreatureCardRoot>
    )
  }
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
