import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import {
  Card as ShadcnCard,
  CardHeader as ShadcnCardHeader,
  CardTitle as ShadcnCardTitle,
  CardContent as ShadcnCardContent,
  CardFooter as ShadcnCardFooter,
} from "@/components/ui/card"

interface CreatureCardProps extends React.ComponentProps<typeof ShadcnCard> {
  uid: string
  name: string
  imageUrl: string
  hp: number
  maxHp: number
}

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, imageUrl, hp, maxHp, ...props }, ref) => (
    <ShadcnCard ref={ref} className={cn("w-64", className)} uid={uid} {...props}>
      <ShadcnCardHeader>
        <ShadcnCardTitle>{name}</ShadcnCardTitle>
      </ShadcnCardHeader>
      <ShadcnCardContent>
        <img src={imageUrl} alt={name} className="w-full h-48 object-cover rounded-md" />
        <div className="mt-4">
          <p>HP: {hp}/{maxHp}</p>
        </div>
      </ShadcnCardContent>
      <ShadcnCardFooter>
        <div className="w-full bg-gray-200 rounded-full h-2.5">
          <div
            className="bg-blue-600 h-2.5 rounded-full"
            style={{ width: `${(hp / maxHp) * 100}%` }}
          ></div>
        </div>
      </ShadcnCardFooter>
    </ShadcnCard>
  )
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
