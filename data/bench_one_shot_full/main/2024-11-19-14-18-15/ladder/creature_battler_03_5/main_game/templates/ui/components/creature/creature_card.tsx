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

let CreatureCardHeader = React.forwardRef<HTMLDivElement, { uid: string } & React.HTMLAttributes<HTMLDivElement>>(
  ({ uid, ...props }, ref) => <CardHeader ref={ref} uid={uid} {...props} />
)

let CreatureCardContent = React.forwardRef<HTMLDivElement, { uid: string } & React.HTMLAttributes<HTMLDivElement>>(
  ({ uid, ...props }, ref) => <CardContent ref={ref} uid={uid} {...props} />
)

let CreatureCardTitle = React.forwardRef<HTMLParagraphElement, { uid: string } & React.HTMLAttributes<HTMLHeadingElement>>(
  ({ uid, ...props }, ref) => <CardTitle ref={ref} uid={uid} {...props} />
)

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, hp, maxHp, imageUrl, ...props }, ref) => {
    return (
      <Card ref={ref} uid={uid} className={cn("w-[300px]", className)} {...props}>
        <CreatureCardHeader uid={`${uid}-header`}>
          <CreatureCardTitle uid={`${uid}-title`}>{name}</CreatureCardTitle>
          <div className="text-sm text-muted-foreground">
            HP: {hp}/{maxHp}
          </div>
        </CreatureCardHeader>
        <CreatureCardContent uid={`${uid}-content`}>
          <img
            src={imageUrl}
            alt={name}
            className="w-full h-[200px] object-contain"
          />
        </CreatureCardContent>
      </Card>
    )
  }
)

CreatureCard.displayName = "CreatureCard"
CreatureCardHeader.displayName = "CreatureCardHeader"
CreatureCardContent.displayName = "CreatureCardContent"
CreatureCardTitle.displayName = "CreatureCardTitle"

CreatureCard = withClickable(CreatureCard)
CreatureCardHeader = withClickable(CreatureCardHeader)
CreatureCardContent = withClickable(CreatureCardContent)
CreatureCardTitle = withClickable(CreatureCardTitle)

export { CreatureCard }
